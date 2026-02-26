import Link from 'next/link';

export default function SubstanceDetailPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Bromantane</h1>
          <nav>
            <Link href="/" className="text-blue-600 hover:text-blue-800 mr-6">Home</Link>
            <Link href="/catalog" className="text-blue-600 hover:text-blue-800 mr-6">Catalog</Link>
            <Link href="/blog" className="text-blue-600 hover:text-blue-800">Blog</Link>
          </nav>
        </div>
      </header>
      
      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="md:col-span-2">
                <div className="mb-8">
                  <h2 className="text-2xl font-semibold text-gray-800 mb-4">Chemical Structure and Classification</h2>
                  <div className="bg-gray-100 border-2 border-dashed rounded-xl w-full h-64 flex items-center justify-center text-gray-500">
                    Molecular Structure Visualization
                  </div>
                </div>
                
                <div className="mb-8">
                  <h2 className="text-2xl font-semibold text-gray-800 mb-4">Mechanism of Action</h2>
                  <div className="prose max-w-none">
                    <p className="text-gray-700 mb-4">
                      Bromantane acts as a selective partial agonist at dopamine D2 and D3 receptors. It also exhibits 
                      actoprotective properties through modulation of stress response pathways and enhancement of 
                      physical and mental performance under stressful conditions.
                    </p>
                    
                    <h3 className="text-lg font-medium text-gray-800 mt-4">Signal Cascade</h3>
                    <ol className="list-decimal pl-6 text-gray-700">
                      <li>Bromantane binds to D2/D3 dopamine receptors with moderate affinity</li>
                      <li>Activation of Gi/o proteins leading to decreased cAMP production</li>
                      <li>Modulation of neuronal excitability in limbic structures</li>
                      <li>Indirect enhancement of dopaminergic neurotransmission</li>
                      <li>Activation of neuroprotective pathways</li>
                      <li>Upregulation of BDNF and other neurotrophic factors</li>
                    </ol>
                  </div>
                </div>
                
                <div className="mb-8">
                  <h2 className="text-2xl font-semibold text-gray-800 mb-4">Pharmacokinetics</h2>
                  <div className="prose max-w-none">
                    <p className="text-gray-700 mb-4">
                      Following oral administration, bromantane is rapidly absorbed with peak plasma concentrations 
                      achieved within 1-2 hours. The compound undergoes hepatic metabolism primarily via CYP enzymes 
                      with a half-life of approximately 6-8 hours.
                    </p>
                    
                    <h3 className="text-lg font-medium text-gray-800 mt-4">Metabolism</h3>
                    <p className="text-gray-700">
                      The primary metabolic pathway involves hydroxylation reactions catalyzed by CYP2D6 and CYP3A4 enzymes. 
                      The metabolites are subsequently conjugated and eliminated through renal excretion.
                    </p>
                  </div>
                </div>
                
                <div className="mb-8">
                  <h2 className="text-2xl font-semibold text-gray-800 mb-4">Clinical Data</h2>
                  <div className="prose max-w-none">
                    <h3 className="text-lg font-medium text-gray-800 mt-4">Preclinical Studies</h3>
                    <p className="text-gray-700 mb-4">
                      Animal studies demonstrate significant actoprotective effects, with improved resistance to 
                      physical and mental stress. Neurochemical analyses reveal increased dopamine turnover in 
                      limbic brain regions and enhanced neuroplasticity markers.
                    </p>
                    
                    <h3 className="text-lg font-medium text-gray-800 mt-4">Clinical Trials</h3>
                    <p className="text-gray-700 mb-4">
                      Phase I/II studies in humans showed good tolerability and demonstrated improvements in 
                      cognitive performance under stress conditions. However, larger-scale trials are needed 
                      to establish definitive therapeutic efficacy.
                    </p>
                    
                    <h3 className="text-lg font-medium text-gray-800 mt-4">Limitations and Contradictions</h3>
                    <p className="text-gray-700">
                      Limited availability of large-scale clinical trials. Some studies suggest variable individual 
                      responses due to genetic polymorphisms in dopamine receptor genes and metabolizing enzymes.
                    </p>
                  </div>
                </div>
                
                <div className="mb-8">
                  <h2 className="text-2xl font-semibold text-gray-800 mb-4">Safety Profile</h2>
                  <div className="prose max-w-none">
                    <p className="text-gray-700 mb-4">
                      Generally well tolerated at therapeutic doses. Common side effects include mild headache, 
                      dizziness, and gastrointestinal discomfort. Long-term safety data is limited.
                    </p>
                    
                    <h3 className="text-lg font-medium text-gray-800 mt-4">Contraindications</h3>
                    <p className="text-gray-700">
                      Contraindicated in patients with known hypersensitivity to the compound, severe cardiovascular 
                      disease, and during pregnancy/lactation.
                    </p>
                  </div>
                </div>
              </div>
              
              <div>
                <div className="bg-gray-50 rounded-lg p-6 mb-6">
                  <h3 className="text-lg font-medium text-gray-800 mb-4">Molecular Properties</h3>
                  <dl className="grid grid-cols-2 gap-x-4 gap-y-3">
                    <dt className="text-sm font-medium text-gray-600">Formula</dt>
                    <dd className="text-sm text-gray-900">C14H22N2O2S</dd>
                    
                    <dt className="text-sm font-medium text-gray-600">Molecular Weight</dt>
                    <dd className="text-sm text-gray-900">282.4 g/mol</dd>
                    
                    <dt className="text-sm font-medium text-gray-600">Class</dt>
                    <dd className="text-sm text-gray-900">Actoprotector</dd>
                    
                    <dt className="text-sm font-medium text-gray-600">Primary Target</dt>
                    <dd className="text-sm text-gray-900">D2/D3 Dopamine Receptors</dd>
                    
                    <dt className="text-sm font-medium text-gray-600">Evidence Level</dt>
                    <dd className="text-sm text-gray-900">Preclinical/Phase II</dd>
                    
                    <dt className="text-sm font-medium text-gray-600">Regulatory Status</dt>
                    <dd className="text-sm text-gray-900">Investigational</dd>
                  </dl>
                </div>
                
                <div className="bg-gray-50 rounded-lg p-6 mb-6">
                  <h3 className="text-lg font-medium text-gray-800 mb-4">Regulatory Status</h3>
                  <ul className="space-y-2">
                    <li className="flex items-start">
                      <span className="mr-2 text-red-500">•</span>
                      <span className="text-sm text-gray-700">Not approved by FDA for any indication</span>
                    </li>
                    <li className="flex items-start">
                      <span className="mr-2 text-red-500">•</span>
                      <span className="text-sm text-gray-700">Not approved by EMA for any indication</span>
                    </li>
                    <li className="flex items-start">
                      <span className="mr-2 text-yellow-500">•</span>
                      <span className="text-sm text-gray-700">Research chemical status in most jurisdictions</span>
                    </li>
                    <li className="flex items-start">
                      <span className="mr-2 text-yellow-500">•</span>
                      <span className="text-sm text-gray-700">Prohibited by WADA as a stimulant</span>
                    </li>
                  </ul>
                </div>
                
                <div className="bg-gray-50 rounded-lg p-6">
                  <h3 className="text-lg font-medium text-gray-800 mb-4">Comparative Analysis</h3>
                  <table className="min-w-full divide-y divide-gray-200">
                    <thead>
                      <tr>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Property</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Bromantane</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Pramipexole</th>
                        <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ISRIB</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200">
                      <tr>
                        <td className="px-4 py-2 text-sm text-gray-700">Primary Target</td>
                        <td className="px-4 py-2 text-sm text-gray-700">D2/D3 Receptors</td>
                        <td className="px-4 py-2 text-sm text-gray-700">D2/D3 Receptors</td>
                        <td className="px-4 py-2 text-sm text-gray-700">eIF2B</td>
                      </tr>
                      <tr>
                        <td className="px-4 py-2 text-sm text-gray-700">Therapeutic Area</td>
                        <td className="px-4 py-2 text-sm text-gray-700">Actoprotector</td>
                        <td className="px-4 py-2 text-sm text-gray-700">Parkinson's, RLS</td>
                        <td className="px-4 py-2 text-sm text-gray-700">Cognitive Enhancement</td>
                      </tr>
                      <tr>
                        <td className="px-4 py-2 text-sm text-gray-700">Evidence Level</td>
                        <td className="px-4 py-2 text-sm text-gray-700">Preclinical</td>
                        <td className="px-4 py-2 text-sm text-gray-700">Approved</td>
                        <td className="px-4 py-2 text-sm text-gray-700">Preclinical</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
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