"""
Task monitoring endpoints for Celery tasks
Provides real-time task status, worker stats, and queue information
"""
from typing import List, Dict, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from celery.result import AsyncResult
from datetime import datetime, timedelta

from app.core.dependencies import get_current_user
from app.models.user import User
from app.celery_app import celery_app

router = APIRouter()


@router.get("/tasks/{task_id}")
async def get_task_status(
    task_id: str,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Get detailed status of a specific Celery task

    Returns task state, result, traceback, and timing information
    """
    task = AsyncResult(task_id, app=celery_app)

    response = {
        "task_id": task_id,
        "state": task.state,
        "ready": task.ready(),
        "successful": task.successful() if task.ready() else None,
        "failed": task.failed() if task.ready() else None,
    }

    # Add result if task is completed
    if task.ready():
        if task.successful():
            response["result"] = task.result
        elif task.failed():
            response["error"] = str(task.info)
            response["traceback"] = task.traceback

    # Add progress info if task is in progress
    elif task.state == 'PROGRESS':
        response["progress"] = task.info

    return response


@router.get("/tasks")
async def list_recent_tasks(
    limit: int = 50,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    List recent tasks with their status

    Note: This requires Celery events to be enabled
    """
    # Get active tasks from Celery workers
    inspect = celery_app.control.inspect()

    active = inspect.active() or {}
    scheduled = inspect.scheduled() or {}
    reserved = inspect.reserved() or {}

    all_tasks = []

    # Process active tasks
    for worker, tasks in active.items():
        for task in tasks:
            all_tasks.append({
                "task_id": task.get('id'),
                "name": task.get('name'),
                "worker": worker,
                "state": "ACTIVE",
                "args": task.get('args'),
                "kwargs": task.get('kwargs'),
                "started_at": task.get('time_start')
            })

    # Process scheduled tasks
    for worker, tasks in scheduled.items():
        for task in tasks:
            all_tasks.append({
                "task_id": task.get('id'),
                "name": task.get('name'),
                "worker": worker,
                "state": "SCHEDULED",
                "eta": task.get('eta')
            })

    # Process reserved tasks
    for worker, tasks in reserved.items():
        for task in tasks:
            all_tasks.append({
                "task_id": task.get('id'),
                "name": task.get('name'),
                "worker": worker,
                "state": "RESERVED"
            })

    return {
        "total_tasks": len(all_tasks),
        "active": sum(1 for t in all_tasks if t.get('state') == 'ACTIVE'),
        "scheduled": sum(1 for t in all_tasks if t.get('state') == 'SCHEDULED'),
        "reserved": sum(1 for t in all_tasks if t.get('state') == 'RESERVED'),
        "tasks": all_tasks[:limit]
    }


@router.get("/workers")
async def get_workers_status(
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Get status of all Celery workers

    Returns worker stats, active queues, and configuration
    """
    inspect = celery_app.control.inspect()

    # Get worker stats
    stats = inspect.stats() or {}
    active_queues = inspect.active_queues() or {}
    registered_tasks = inspect.registered() or {}
    ping = celery_app.control.ping(timeout=1.0) or []

    workers = []

    for worker_name, worker_stats in stats.items():
        workers.append({
            "name": worker_name,
            "status": "online" if any(w.get(worker_name) for w in ping) else "offline",
            "pool": worker_stats.get('pool', {}).get('implementation'),
            "max_concurrency": worker_stats.get('pool', {}).get('max-concurrency'),
            "total_tasks_completed": worker_stats.get('total', {}),
            "queues": [q.get('name') for q in active_queues.get(worker_name, [])],
            "registered_tasks": len(registered_tasks.get(worker_name, []))
        })

    return {
        "total_workers": len(workers),
        "online": sum(1 for w in workers if w.get('status') == 'online'),
        "offline": sum(1 for w in workers if w.get('status') == 'offline'),
        "workers": workers
    }


@router.get("/queues")
async def get_queues_status(
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Get status of all Celery queues

    Returns message counts and queue configuration
    """
    inspect = celery_app.control.inspect()
    active_queues = inspect.active_queues() or {}

    queues = {}

    # Aggregate queues from all workers
    for worker, worker_queues in active_queues.items():
        for queue in worker_queues:
            queue_name = queue.get('name')
            if queue_name not in queues:
                queues[queue_name] = {
                    "name": queue_name,
                    "workers": [],
                    "routing_key": queue.get('routing_key'),
                    "exchange": queue.get('exchange', {}).get('name')
                }
            queues[queue_name]["workers"].append(worker)

    return {
        "total_queues": len(queues),
        "queues": list(queues.values())
    }


@router.get("/scheduled")
async def get_scheduled_tasks(
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Get all scheduled (beat) tasks configuration

    Returns Celery Beat schedule with next run times
    """
    from celery import current_app

    schedule = current_app.conf.beat_schedule or {}

    scheduled_tasks = []

    for task_name, task_config in schedule.items():
        scheduled_tasks.append({
            "name": task_name,
            "task": task_config.get('task'),
            "schedule": str(task_config.get('schedule')),
            "args": task_config.get('args', []),
            "kwargs": task_config.get('kwargs', {}),
            "options": task_config.get('options', {})
        })

    return {
        "total_scheduled": len(scheduled_tasks),
        "tasks": scheduled_tasks
    }


@router.post("/tasks/{task_id}/cancel")
async def cancel_task(
    task_id: str,
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Cancel a running or pending task

    Note: This sends a terminate signal to the task
    """
    celery_app.control.revoke(task_id, terminate=True, signal='SIGKILL')

    return {
        "message": "Task cancellation requested",
        "task_id": task_id
    }


@router.get("/stats")
async def get_system_stats(
    current_user: User = Depends(get_current_user)
) -> Dict:
    """
    Get overall system statistics

    Aggregated stats from all workers and queues
    """
    inspect = celery_app.control.inspect()

    active = inspect.active() or {}
    scheduled = inspect.scheduled() or {}
    stats = inspect.stats() or {}

    total_active = sum(len(tasks) for tasks in active.values())
    total_scheduled = sum(len(tasks) for tasks in scheduled.values())
    total_workers = len(stats)

    # Calculate total tasks processed
    total_processed = 0
    for worker_stats in stats.values():
        total_processed += sum(worker_stats.get('total', {}).values())

    return {
        "workers": {
            "total": total_workers,
            "online": total_workers  # All workers in stats are online
        },
        "tasks": {
            "active": total_active,
            "scheduled": total_scheduled,
            "total_processed": total_processed
        },
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/health")
async def health_check() -> Dict:
    """
    Health check endpoint for monitoring systems

    Checks if Celery workers are responsive
    """
    try:
        # Ping workers with 3 second timeout
        ping_result = celery_app.control.ping(timeout=3.0)

        if ping_result:
            return {
                "status": "healthy",
                "workers_online": len(ping_result),
                "timestamp": datetime.utcnow().isoformat()
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="No Celery workers available"
            )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Celery workers unreachable: {str(e)}"
        )
