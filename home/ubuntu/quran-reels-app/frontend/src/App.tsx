
import { useState } from 'react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Toaster } from "@/components/ui/sonner"
import { Button } from "@/components/ui/button"
import { Home, Settings, Image } from "lucide-react"

function App() {
  const [processing, setProcessing] = useState(false);

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-900">
      <header className="bg-white dark:bg-zinc-950 shadow-sm py-4">
        <div className="container mx-auto px-4">
          <h1 className="text-2xl font-bold text-zinc-900 dark:text-zinc-50">تطبيق ريلز القرآن</h1>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <Tabs defaultValue="upload" className="w-full">
          <TabsList className="mb-6">
            <TabsTrigger value="upload" className="flex items-center gap-2">
              <Home className="h-4 w-4" />
              <span>الرئيسية</span>
            </TabsTrigger>
            <TabsTrigger value="gallery" className="flex items-center gap-2">
              <Image className="h-4 w-4" />
              <span>معرض الفيديوهات</span>
            </TabsTrigger>
            <TabsTrigger value="settings" className="flex items-center gap-2">
              <Settings className="h-4 w-4" />
              <span>الإعدادات</span>
            </TabsTrigger>
          </TabsList>
          
          <TabsContent value="upload" className="space-y-6">
            <div className="bg-white dark:bg-zinc-950 rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-semibold mb-4 text-right">رفع تسجيل صوتي</h2>
              <div className="border-2 border-dashed border-zinc-200 dark:border-zinc-800 rounded-lg p-8 text-center">
                <p className="text-zinc-600 dark:text-zinc-400 mb-4">اسحب وأفلت الملف الصوتي هنا أو انقر لاختيار ملف</p>
                <Button variant="default">اختيار ملف</Button>
              </div>

              <div className="mt-6">
                <Button 
                  className="w-full" 
                  disabled={processing}
                  onClick={() => setProcessing(true)}
                >
                  {processing ? 'جاري المعالجة...' : 'إنشاء فيديو ريلز'}
                </Button>
              </div>
            </div>
          </TabsContent>
          
          <TabsContent value="gallery">
            <div className="bg-white dark:bg-zinc-950 rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-semibold mb-4 text-right">معرض الفيديوهات</h2>
              <p className="text-zinc-600 dark:text-zinc-400 text-center py-8">لا توجد فيديوهات متاحة حالياً</p>
            </div>
          </TabsContent>
          
          <TabsContent value="settings">
            <div className="bg-white dark:bg-zinc-950 rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-semibold mb-4 text-right">الإعدادات</h2>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-zinc-600 dark:text-zinc-400">الوضع الداكن</span>
                  <div>{/* سيتم إضافة مفتاح التبديل هنا */}</div>
                </div>
              </div>
            </div>
          </TabsContent>
        </Tabs>
      </main>
      
      <Toaster />
    </div>
  )
}

export default App
