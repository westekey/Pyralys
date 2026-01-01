'use client'

import { useState, useEffect } from 'react'
import { billingApi } from '@/lib/billing'
import { Button } from '@/components/ui/button'

export default function BillingPage() {
  const [plans, setPlans] = useState<any>(null)
  const [subscription, setSubscription] = useState<any>(null)
  const [invoices, setInvoices] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadBillingData()
  }, [])

  const loadBillingData = async () => {
    try {
      setLoading(true)
      const [plansData, subData, invoicesData] = await Promise.all([
        billingApi.getPlans(),
        billingApi.getSubscription(),
        billingApi.getInvoices()
      ])
      setPlans(plansData)
      setSubscription(subData)
      setInvoices(invoicesData)
    } catch (error) {
      console.error('Error loading billing data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleUpgrade = async (planType: string) => {
    try {
      const { url } = await billingApi.createCheckout(planType)
      window.location.href = url
    } catch (error) {
      console.error('Error creating checkout:', error)
      alert('Failed to start checkout process')
    }
  }

  const handleManageSubscription = async () => {
    try {
      const { url } = await billingApi.createPortal()
      window.location.href = url
    } catch (error) {
      console.error('Error opening portal:', error)
      alert('Failed to open customer portal')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
          <p className="text-gray-600">Loading billing...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold mb-2">Billing & Subscription</h1>
        <p className="text-gray-600">
          Manage your subscription and billing information
        </p>
      </div>

      {/* Current Subscription */}
      {subscription && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <div className="flex justify-between items-start mb-4">
            <div>
              <h2 className="text-xl font-semibold mb-2">Current Plan</h2>
              <div className="flex items-center gap-3">
                <span className="text-2xl font-bold capitalize">{subscription.plan_type}</span>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  subscription.status === 'active' ? 'bg-green-100 text-green-800' :
                  subscription.status === 'trialing' ? 'bg-blue-100 text-blue-800' :
                  subscription.status === 'past_due' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {subscription.status}
                </span>
              </div>
            </div>
            {subscription.stripe_subscription_id && (
              <Button onClick={handleManageSubscription} variant="outline">
                Manage Subscription
              </Button>
            )}
          </div>

          {subscription.current_period_end && (
            <p className="text-sm text-gray-600">
              {subscription.cancel_at_period_end
                ? `Cancels on ${new Date(subscription.current_period_end).toLocaleDateString()}`
                : `Renews on ${new Date(subscription.current_period_end).toLocaleDateString()}`
              }
            </p>
          )}
        </div>
      )}

      {/* Available Plans */}
      {plans && plans.plans && (
        <div>
          <h2 className="text-xl font-semibold mb-4">Available Plans</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {plans.plans.map((plan: any) => (
              <PlanCard
                key={plan.name}
                plan={plan}
                currentPlan={subscription?.plan_type}
                onUpgrade={handleUpgrade}
              />
            ))}
          </div>
        </div>
      )}

      {/* Invoices */}
      {invoices.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h2 className="text-xl font-semibold mb-4">Billing History</h2>
          <div className="space-y-3">
            {invoices.map((invoice) => (
              <div key={invoice.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                <div>
                  <p className="font-medium">
                    ${(invoice.amount_paid / 100).toFixed(2)} {invoice.currency.toUpperCase()}
                  </p>
                  <p className="text-sm text-gray-600">
                    {new Date(invoice.invoice_date).toLocaleDateString()}
                  </p>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`px-3 py-1 rounded-full text-sm ${
                    invoice.status === 'paid' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {invoice.status}
                  </span>
                  {invoice.hosted_invoice_url && (
                    <a
                      href={invoice.hosted_invoice_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline text-sm"
                    >
                      View Invoice
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

// PlanCard Component
function PlanCard({
  plan,
  currentPlan,
  onUpgrade
}: {
  plan: any
  currentPlan: string
  onUpgrade: (planType: string) => void
}) {
  const isCurrentPlan = plan.name.toLowerCase() === currentPlan
  const isFree = plan.price === 0

  return (
    <div className={`border-2 rounded-lg p-6 ${
      isCurrentPlan ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
    }`}>
      <div className="mb-4">
        <h3 className="text-xl font-bold mb-2">{plan.name}</h3>
        <div className="flex items-baseline gap-1">
          <span className="text-3xl font-bold">${(plan.price / 100).toFixed(0)}</span>
          <span className="text-gray-600">/{plan.interval}</span>
        </div>
      </div>

      <ul className="space-y-2 mb-6">
        {plan.features.map((feature: string, index: number) => (
          <li key={index} className="flex items-start gap-2 text-sm">
            <span className="text-green-600 mt-0.5">✓</span>
            <span>{feature}</span>
          </li>
        ))}
      </ul>

      {isCurrentPlan ? (
        <Button disabled className="w-full">
          Current Plan
        </Button>
      ) : isFree ? (
        <Button variant="outline" disabled className="w-full">
          Free
        </Button>
      ) : (
        <Button
          onClick={() => onUpgrade(plan.name.toLowerCase())}
          className="w-full"
        >
          Upgrade
        </Button>
      )}
    </div>
  )
}
