import Link from 'next/link';

export default function BlogPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Analytical Blog</h1>
          <nav>
            <Link href="/" className="text-blue-600 hover:text-blue-800 mr-6">Home</Link>
            <Link href="/catalog" className="text-blue-600 hover:text-blue-800 mr-6">Catalog</Link>
            <Link href="/about" className="text-blue-600 hover:text-blue-800">About</Link>
          </nav>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="mb-8">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">Categories</h2>
              <div className="flex flex-wrap gap-2">
                <button className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm">Neuroplasticity</button>
                <button className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">Stress Response</button>
                <button className="px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm">Dopamine System</button>
                <button className="px-3 py-1 bg-purple-100 text-purple-800 rounded-full text-sm">Actoprotection</button>
                <button className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm">Research Paradigms</button>
                <button className="px-3 py-1 bg-indigo-100 text-indigo-800 rounded-full text-sm">PROTACs</button>
              </div>
            </div>
            
            <div className="mt-8">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">Latest Articles</h2>
              <div className="space-y-6">
                <article className="border border-gray-200 rounded-lg p-6 hover:bg-gray-50">
                  <h3 className="text-xl font-medium text-gray-900 mb-2">Why Genomic Induction of Dopamine Is Not the Same as Stimulation</h3>
                  <div className="flex items-center text-sm text-gray-500 mb-3">
                    <span>January 15, 2026</span>
                    <span className="mx-2">•</span>
                    <span>12 min read</span>
                  </div>
                  <p className="text-gray-600 mb-4">
                    A critical analysis of the differences between genomic induction mechanisms and direct receptor stimulation in dopaminergic pathways...
                  </p>
                  <div className="flex space-x-2">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      Dopamine System
                    </span>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                      Mechanism Analysis
                    </span>
                  </div>
                </article>
                
                <article className="border border-gray-200 rounded-lg p-6 hover:bg-gray-50">
                  <h3 className="text-xl font-medium text-gray-900 mb-2">ISR: Protective Mechanism or Pathology?</h3>
                  <div className="flex items-center text-sm text-gray-500 mb-3">
                    <span>January 10, 2026</span>
                    <span className="mx-2">•</span>
                    <span>15 min read</span>
                  </div>
                  <p className="text-gray-600 mb-4">
                    Exploring the dual nature of the Integrated Stress Response and its role in neuroprotection versus neurodegeneration...
                  </p>
                  <div className="flex space-x-2">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      Stress Response
                    </span>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                      Critical Review
                    </span>
                  </div>
                </article>
                
                <article className="border border-gray-200 rounded-lg p-6 hover:bg-gray-50">
                  <h3 className="text-xl font-medium text-gray-900 mb-2">Allosteric Modulation as the Future of Pharmacology</h3>
                  <div className="flex items-center text-sm text-gray-500 mb-3">
                    <span>January 5, 2026</span>
                    <span className="mx-2">•</span>
                    <span>18 min read</span>
                  </div>
                  <p className="text-gray-600 mb-4">
                    Examining how allosteric modulators offer superior selectivity and safety profiles compared to orthosteric ligands...
                  </p>
                  <div className="flex space-x-2">
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                      Research Paradigms
                    </span>
                    <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                      Allosteric Modulation
                    </span>
                  </div>
                </article>
              </div>
            </div>
          </div>
        </div>
      </main>
      
      <footer className="bg-white mt-8 py-6 border-t">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-center text-gray-500 text-sm">
            Information provided for educational purposes only. Not medical advice.
          </p>
        </div>
      </footer>
    </div>
  );
}