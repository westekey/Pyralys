'use client'

import { useState } from 'react'
import { AIAPI } from '@/lib/ai'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import toast from 'react-hot-toast'

type GenerationType = 'caption' | 'image' | 'hashtags'

export default function GeneratePage() {
  const [generationType, setGenerationType] = useState<GenerationType>('caption')
  const [prompt, setPrompt] = useState('')
  const [platform, setPlatform] = useState<'instagram' | 'tiktok' | 'linkedin' | 'facebook'>('instagram')
  const [tone, setTone] = useState<'casual' | 'professional' | 'funny' | 'inspirational'>('casual')
  const [style, setStyle] = useState('realistic')
  const [size, setSize] = useState<'1024x1024' | '1024x1792' | '1792x1024'>('1024x1024')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<any>(null)

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      toast.error('Please enter a prompt')
      return
    }

    setLoading(true)
    setResult(null)

    try {
      let data: any

      if (generationType === 'caption') {
        data = await AIAPI.generateCaption({ prompt, platform, tone })
        toast.success('Caption generated successfully!')
      } else if (generationType === 'image') {
        data = await AIAPI.generateImage({ prompt, style, size, platform })
        toast.success('Image generated successfully!')
      } else {
        data = await AIAPI.generateHashtags({ topic: prompt, platform, count: 15 })
        toast.success('Hashtags generated successfully!')
      }

      setResult(data)
    } catch (error: any) {
      console.error('Generation failed:', error)
      if (error.response?.status === 403) {
        toast.error('This feature requires a premium plan. Please upgrade!')
      } else {
        toast.error(error.response?.data?.detail || 'Generation failed')
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">AI Content Generator</h1>
        <p className="text-gray-600">
          Create amazing captions, images, and hashtags with AI
        </p>
      </div>

      <div className="grid lg:grid-cols-2 gap-8">
        {/* Input Panel */}
        <div className="bg-white rounded-lg shadow-md p-6 space-y-6">
          <div>
            <Label className="text-base font-semibold mb-3 block">
              What do you want to generate?
            </Label>
            <div className="grid grid-cols-3 gap-2">
              <Button
                variant={generationType === 'caption' ? 'default' : 'outline'}
                onClick={() => setGenerationType('caption')}
                className="w-full"
              >
                Caption
              </Button>
              <Button
                variant={generationType === 'image' ? 'default' : 'outline'}
                onClick={() => setGenerationType('image')}
                className="w-full"
              >
                Image
              </Button>
              <Button
                variant={generationType === 'hashtags' ? 'default' : 'outline'}
                onClick={() => setGenerationType('hashtags')}
                className="w-full"
              >
                Hashtags
              </Button>
            </div>
          </div>

          <div>
            <Label htmlFor="prompt">
              {generationType === 'hashtags' ? 'Topic' : 'Prompt'}
            </Label>
            <textarea
              id="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder={
                generationType === 'caption'
                  ? 'Describe your post idea... (e.g., "Sunset at the beach with friends")'
                  : generationType === 'image'
                  ? 'Describe the image you want... (e.g., "A futuristic AI tower glowing at night")'
                  : 'Enter your main topic... (e.g., "fitness motivation")'
              }
              className="w-full min-h-[120px] px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            />
          </div>

          <div>
            <Label htmlFor="platform">Platform</Label>
            <select
              id="platform"
              value={platform}
              onChange={(e) => setPlatform(e.target.value as any)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
            >
              <option value="instagram">Instagram</option>
              <option value="tiktok">TikTok</option>
              <option value="linkedin">LinkedIn</option>
              <option value="facebook">Facebook</option>
            </select>
          </div>

          {generationType === 'caption' && (
            <div>
              <Label htmlFor="tone">Tone</Label>
              <select
                id="tone"
                value={tone}
                onChange={(e) => setTone(e.target.value as any)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value="casual">Casual</option>
                <option value="professional">Professional</option>
                <option value="funny">Funny</option>
                <option value="inspirational">Inspirational</option>
              </select>
            </div>
          )}

          {generationType === 'image' && (
            <>
              <div>
                <Label htmlFor="style">Style</Label>
                <select
                  id="style"
                  value={style}
                  onChange={(e) => setStyle(e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="realistic">Realistic</option>
                  <option value="artistic">Artistic</option>
                  <option value="minimal">Minimal</option>
                  <option value="vibrant">Vibrant</option>
                  <option value="corporate">Corporate</option>
                  <option value="vintage">Vintage</option>
                  <option value="3d">3D Render</option>
                </select>
              </div>

              <div>
                <Label htmlFor="size">Size</Label>
                <select
                  id="size"
                  value={size}
                  onChange={(e) => setSize(e.target.value as any)}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="1024x1024">Square (1024x1024)</option>
                  <option value="1024x1792">Portrait (1024x1792)</option>
                  <option value="1792x1024">Landscape (1792x1024)</option>
                </select>
              </div>
            </>
          )}

          <Button
            onClick={handleGenerate}
            disabled={loading}
            className="w-full"
            size="lg"
          >
            {loading ? 'Generating...' : `Generate ${generationType}`}
          </Button>
        </div>

        {/* Result Panel */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-bold mb-4">Result</h2>

          {!result && (
            <div className="flex items-center justify-center h-64 text-gray-400">
              <div className="text-center">
                <div className="text-6xl mb-4">✨</div>
                <p>Your generated content will appear here</p>
              </div>
            </div>
          )}

          {result && generationType === 'caption' && (
            <div className="space-y-4">
              <div>
                <Label className="text-sm font-semibold mb-2 block">
                  Caption
                </Label>
                <div className="p-4 bg-gray-50 rounded-md whitespace-pre-wrap">
                  {result.caption}
                </div>
              </div>

              <div>
                <Label className="text-sm font-semibold mb-2 block">
                  Hashtags ({result.hashtags.length})
                </Label>
                <div className="p-4 bg-gray-50 rounded-md flex flex-wrap gap-2">
                  {result.hashtags.map((tag: string, i: number) => (
                    <span
                      key={i}
                      className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>

              <Button variant="outline" className="w-full">
                Copy to Clipboard
              </Button>
            </div>
          )}

          {result && generationType === 'image' && (
            <div className="space-y-4">
              <div>
                <img
                  src={result.image_url}
                  alt="Generated image"
                  className="w-full rounded-md"
                />
              </div>

              <div>
                <Label className="text-sm font-semibold mb-2 block">
                  AI Revised Prompt
                </Label>
                <div className="p-4 bg-gray-50 rounded-md text-sm">
                  {result.revised_prompt}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2">
                <Button variant="outline" className="w-full">
                  Download
                </Button>
                <Button className="w-full">Save to Library</Button>
              </div>
            </div>
          )}

          {result && generationType === 'hashtags' && (
            <div className="space-y-4">
              <div>
                <Label className="text-sm font-semibold mb-2 block">
                  Generated Hashtags ({result.count})
                </Label>
                <div className="p-4 bg-gray-50 rounded-md flex flex-wrap gap-2">
                  {result.hashtags.map((tag: string, i: number) => (
                    <span
                      key={i}
                      className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>

              <Button variant="outline" className="w-full">
                Copy All
              </Button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
