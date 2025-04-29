# The 1st free5GC World Forum 2025

<div class="banner">
  <div class="banner-overlay">
    <h1>The 1st free5GC World Forum</h1>
    <p>In conjunction with ACM CCS 2025</p>
    <p>October 13, 2025 • Taipei, Taiwan</p>
    <a href="https://www.sigsac.org/ccs/CCS2025/" class="banner-button">Visit ACM CCS 2025</a>
  </div>
</div>

<style>
.cta-button {
  display: inline-block;
  background-color: #e74c3c;
  color: white !important;
  text-decoration: none;
  padding: 0.8rem 1.5rem;
  border-radius: 4px;
  font-weight: bold;
  margin-top: 1rem;
  transition: background-color 0.3s, transform 0.2s;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.cta-button:hover {
  background-color: #c0392b;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

.cta-button svg {
  width: 16px;
  height: 16px;
  vertical-align: middle;
  margin-right: 8px;
}

.cta-section {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 2rem;
  border-radius: 8px;
  margin: 2rem 0;
  text-align: center;
  border-left: 4px solid #3498db;
}

.cta-section h2 {
  color: #2c3e50 !important;
  font-weight: bold !important;
  margin-top: 0;
}

.cta-section p {
  max-width: 800px;
  margin: 1rem auto;
}

.banner {
  position: relative;
  width: 100%;
  height: 300px;
  background-image: url('https://free5gc.org/assets/background.jpg');
  background-size: cover;
  background-position: center;
  margin-bottom: 2rem;
  border-radius: 8px;
  overflow: hidden;
}

.banner-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 80, 0.7) !important;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
}

.banner-overlay h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
  color: white;
}

.banner-overlay p {
  font-size: 1.2rem;
  margin: 0.3rem 0;
}

.banner-button {
  margin-top: 1.5rem;
  padding: 0.8rem 1.5rem;
  background-color: #e74c3c !important;
  color: white !important;
  text-decoration: none;
  border-radius: 4px;
  font-weight: bold;
  transition: background-color 0.3s;
}

.banner-button:hover {
  background-color: #c0392b !important;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
  margin: 2rem 0;
}

.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.card h3 {
  color: #2c3e50;
  margin-top: 0;
  border-bottom: 2px solid #3498db;
  padding-bottom: 0.5rem;
}

.card ul {
  padding-left: 1.2rem;
}

.timeline {
  position: relative;
  max-width: 800px;
  margin: 2rem auto;
}

.timeline::after {
  content: '';
  position: absolute;
  width: 6px;
  background-color: #3498db;
  top: 0;
  bottom: 0;
  left: 50%;
  margin-left: -3px;
  border-radius: 3px;
}

.timeline-item {
  padding: 10px 40px;
  position: relative;
  width: 50%;
  box-sizing: border-box;
}

.timeline-item::after {
  content: '';
  position: absolute;
  width: 20px;
  height: 20px;
  background-color: white;
  border: 4px solid #3498db;
  border-radius: 50%;
  top: 15px;
  right: -14px;
  z-index: 1;
}

.timeline-item:nth-child(odd) {
  left: 0;
}

.timeline-item:nth-child(even) {
  left: 50%;
}

.timeline-item:nth-child(even)::after {
  left: -14px;
}

.timeline-content {
  padding: 15px;
  background-color: white;
  border-radius: 6px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.timeline-content h3 {
  margin-top: 0;
  color: #3498db;
}

.committee-section {
  margin: 2rem 0;
}

.committee-members {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.committee-member {
  background-color: #f8f9fa;
  border-radius: 6px;
  padding: 1rem;
  flex: 1 0 300px;
}

.committee-member h4 {
  margin-top: 0;
  color: #2c3e50;
}

.card h3 {
  color: #2c3e50;
  margin-top: 0;
  border-bottom: 2px solid #3498db;
  padding-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.topic-icon {
  width: 24px;
  height: 24px;
  min-width: 24px;
  fill: #3498db;
}


.card h3 svg {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}


@media screen and (max-width: 768px) {
  .banner-overlay h1 {
    font-size: 1.8rem;
  }

  .banner-overlay p {
    font-size: 1rem;
  }

  .banner-button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    background-color: #e74c3c !important;
  }

  .timeline::after {
    left: 31px;
  }
  
  .timeline-item {
    width: 100%;
    padding-left: 70px;
    padding-right: 25px;
  }
  
  .timeline-item:nth-child(even) {
    left: 0;
  }
  
  .timeline-item:nth-child(even)::after,
  .timeline-item::after {
    left: 17px;
  }
}
</style>


## About the Forum

<div class="cta-section">
  <h2>Call for Papers</h2>
  <p>We invite submissions for the 1st free5GC World Forum. The forum seeks original, unpublished papers focusing on security, architecture, innovation, and real-world applications of 5G core networks, particularly those leveraging the free5GC platform.</p>
  <p>Submission deadline: <strong>June 20, 2025</strong></p>
  <a href="https://github.com/free5gc/free5gc.github.io/blob/forum-cfp/free5GC-forum-cfp.pdf" class="cta-button" target="_blank">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
      <path d="M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z"/>
    </svg>
    Download CFP PDF
  </a>
</div>

We are pleased to announce the 1st free5GC World Forum, to be held in conjunction with ACM Conference on Computer and Communications Security (CCS) 2025 ([https://www.sigsac.org/ccs/CCS2025/](https://www.sigsac.org/ccs/CCS2025/)), one of the premier conferences in cybersecurity. This forum will bring together researchers, industry professionals, and open-source contributors to explore the challenges and recent advancements in 5G core networks, with a particular focus on security and the transformative role of free5GC, the leading open-source 5G Standalone (SA) core network. 

free5GC ([https://free5gc.org/](https://free5gc.org/)), a project hosted by the Linux Foundation, is a fully 3GPP-compliant open-source 5G core network platform. It empowers researchers, developers, and businesses to drive innovation in 5G systems, providing a robust prototyping environment for next-generation connectivity solutions. Recent notable architectures such as L25GC+ ([https://github.com/nycu-ucr/L25GC-plus](https://github.com/nycu-ucr/L25GC-plus)), which aim to significantly reduce control plane latency while maintaining 3GPP compliance, exemplify how free5GC facilitates the development and testing of cutting-edge ideas on a production-grade 5G core.

The forum will provide a unique opportunity for participants to share insights, present innovations, and shape the future direction of free5GC and next-generation mobile networks.

Submissions will be evaluated based on technical rigor, novelty, and relevance to 5G core networks. Priority will be given to papers that demonstrate practical security implications, novel attack models, performance improvements, or defense mechanisms applicable to free5GC, L25GC+, and related platforms.

## Topics of Interest

We invite original research papers, technical reports, and case studies in, but not limited to, the following areas:

<div class="grid-container">
  <div class="card">
    <h3>5G Security</h3>
    <ul>
        <li>Security and Privacy in 5G Core Networks</li>
        <li>Threat Modeling and Attack Detection for free5GC</li>
        <li>Secure Network Slicing and Isolation</li>
        <li>Authentication and Access Control in 5G</li>
        <li>Zero Trust Architectures for 5G Core Networks</li>
        <li>AI/ML for Anomaly Detection in free5GC</li>
        <li>Denial-of-Service (DoS) Mitigation in 5G Core</li>
        <li>End-to-End Security in 5G and Beyond</li>
        <li>Post-Quantum Cryptography for 5G Core</li>
        <li>Security of Interoperability Between 5G and Legacy Networks</li>
        <li>Forensics and Incident Response in 5G Core Networks</li>
    </ul>
  </div>
  <div class="card">
    <h3>Network Architecture and Innovation</h3>
    <ul>
        <li>NFV and Container Security in 5G Deployments</li>
        <li>Low-Latency 5G Core Architectures (e.g., L25GC+)</li>
        <li>free5GC Development and Enhancements</li>
        <li>5G Standalone (SA) Core Networks</li>
        <li>Next-Generation Cellular Network Architectures</li>
        <li>Network Slicing and Virtualized Core Networks</li>
        <li>Edge Computing and MEC Integration</li>
        <li>AI/ML for Network Optimization</li>
        <li>6G Vision and Future Core Networks</li>
        <li>Interoperability and Multi-Vendor Deployments</li>
        <li>5G Core Support for Private Cellular Networks</li>
        <li>5G Core Support in Multi-Operator Network Scenarios</li>
    </ul>
  </div>
  <div class="card">
    <h3>Real-World Use Cases of free5GC</h3>
    <ul>
        <li>Real-World Deployments and Use Cases of free5GC</li>
        <li>Open-Source Project integration with free5GC</li>
    </ul>
  </div>
</div>

## Submission Guidelines

- Submitted papers must not substantially overlap papers that have been published or that are simultaneously submitted to a journal or a conference with proceedings.
- Long papers: Maximum 12 pages for review, with the final camera-ready version limited to 9 pages. Submissions should be no more than 12 pages in the ACM double-column format, excluding the bibliography and well-marked appendix. Committee members are not required to read the appendices, so the paper should be understandable without them. For accepted papers, the final camera-ready version may be limited to 9 pages, including the bibliography, appendix, and all content.
- Short papers: 4 pages for both review and final camera-ready submission. The forum also welcomes short submissions of up to 4 pages for preliminary results or concise contributions that can be clearly described in a few pages.
- Authors of long-paper submissions may indicate in a footnote on the first page if they would like their paper to also be considered for publication as a short paper (4 pages in the proceedings).
- Submissions must be PDF files in the ACM double-column format ([https://www.acm.org/publications/proceedings-template](https://www.acm.org/publications/proceedings-template)) using the “sigconf” template. Authors should not modify the font or margins of the ACM format. The CCS information such as concepts, keywords, or rights management data (e.g., DOI, ISBN) must be included. A teaser figure is optional. Please refer to sample-sigconf.tex and sample-sigconf.pdf in the ACM LaTeX package ([https://www.overleaf.com/latex/templates/association-for-computing-machinery-acm-sig-proceedings-template/bmvfhcdnxfty](https://www.overleaf.com/latex/templates/association-for-computing-machinery-acm-sig-proceedings-template/bmvfhcdnxfty)) for formatting examples. Submissions not following the required format may be rejected without review.
- Submissions should not be anonymized.
- Submissions are to be made to the submission website at HotCRP ([https://free5gc-2025.hotcrp.com/](https://free5gc-2025.hotcrp.com/)). Only PDF files will be accepted. Submissions not meeting these guidelines risk rejection without consideration of their merits.
- Authors of accepted papers must ensure that their paper will be presented at the forum by at least one of the authors.

> [!NOTE]
> Authors of accepted papers must guarantee that their paper will be presented at the workshop.

## Important Dates

<div class="timeline">
  <div class="timeline-item">
    <div class="timeline-content">
      <h3>Paper Submission Deadline</h3>
        <p>June 20, 2025</p>
    </div>
  </div>
  <div class="timeline-item">
    <div class="timeline-content">
      <h3>Notification of Acceptance</h3>
      <p>August 8, 2025</p>
    </div>
  </div>
  <div class="timeline-item">
    <div class="timeline-content">
      <h3>Camera-Ready Papers Due</h3>
      <p>August 22, 2025</p>
    </div>
  </div>
  <div class="timeline-item">
    <div class="timeline-content">
      <h3>Forum Date</h3>
      <p>October 13, 2025</p>
    </div>
  </div>
</div>

## Venue

The 1st free5GC World Forum will take place in conjunction with ACM CCS 2025 in Taipei, Taiwan, offering opportunities for in-depth discussions and collaboration on securing 5G core networks.

## Visa

Before traveling to Taiwan, please review the visa requirements and ensure that you have a valid visa. For detailed information, please visit: [https://www.sigsac.org/ccs/CCS2025/visa/](https://www.sigsac.org/ccs/CCS2025/visa/).

## Organizing Committee

<div class="committee-section">
  <h3>General Chairs</h3>
  <div class="committee-members">
    <div class="committee-member">
      <h4>Jyh-Cheng Chen</h4>
      <p>National Yang Ming Chiao Tung University (NYCU)</p>
    </div>
    <div class="committee-member">
      <h4>K. K. Ramakrishnan</h4>
      <p>University of California, Riverside</p>
    </div>
  </div>
</div>

<div class="committee-section">
  <h3>International Advisory Committee</h3>
  <div class="committee-members">
    <div class="committee-member">
      <h4>Falko Dressler</h4>
      <p>TU Berlin</p>
    </div>
    <div class="committee-member">
      <h4>Tommaso Melodia</h4>
      <p>Northeastern University</p>
    </div>
    <div class="committee-member">
      <h4>Akihiro Nakao</h4>
      <p>The University of Tokyo</p>
    </div>
    <div class="committee-member">
      <h4>Shivendra Panwar</h4>
      <p>Tandon School of Engineering of New York University</p>
    </div>
    <div class="committee-member">
      <h4>Ashutosh Sabharwal</h4>
      <p>Rice University</p>
    </div>
    <div class="committee-member">
      <h4>Gil Zussman</h4>
      <p>Columbia University</p>
    </div>
  </div>
</div>

<div class="committee-section">
  <h3>Technical Program Committee Chair</h3>
  <div class="committee-members">
    <div class="committee-member">
      <h4>Chien Chen</h4>
      <p>National Yang Ming Chiao Tung University (NYCU)</p>
    </div>
  </div>
</div>

<div class="committee-section">
  <h3>Publicity Chairs</h3>
  <div class="committee-members">
    <div class="committee-member">
      <h4>Chi-Yu Li</h4>
      <p>National Yang Ming Chiao Tung University (NYCU)</p>
    </div>
    <div class="committee-member">
      <h4>Shixiong Qi</h4>
      <p>University of Kentucky</p>
    </div>
  </div>
</div>

<div class="committee-section">
  <h3>Web Chair</h3>
  <div class="committee-members">
    <div class="committee-member">
      <h4>Yi Chen</h4>
      <p>National Yang Ming Chiao Tung University (NYCU)</p>
    </div>
  </div>
</div>

<div class="committee-section">
  <h3>Program Committee Members</h3>
  <div class="committee-members">
    <div class="committee-member">
      <p>Chien Chen, National Yang Ming Chiao Tung University (NYCU)</p>
      <p>Yi Chen, National Yang Ming Chiao Tung University (NYCU)</p>
      <p>Nakjung Choi, Nokia Bell Labs</p>
      <p>Rahman Doost-Mohammady, Rice University</p>
      <p>Ashutosh Dutta, Johns Hopkins University</p>
      <p>Xinyu Lei, Michigan Technological University</p>
      <p>Chi-Yu Li, National Yang Ming Chiao Tung University (NYCU)</p>
      <p>Fuchun Joseph Lin, National Yang Ming Chiao Tung University (NYCU)</p>
      <p>Chunyi Peng, Purdue University</p>
      <p>Shixiong Qi, University of Kentucky</p>
      <p>Yuji Sekiya, The University of Tokyo</p>
      <p>Ivan Seskar, Rutgers University</p>
      <p>Zhaowei Tan, University of California, Riverside</p>
      <p>Chien-Chao Tseng,  National Yang Ming Chiao Tung University (NYCU)</p>
      <p>Guan-Hua Tu, Michigan State University</p>
      <p>Yang Xiao, University of Kentucky</p>
      <p>Tian Xie, Utah State University</p>
      <p>Lou Yang, National Yang Ming Chiao Tung University (NYCU)</p>
      <p>Antonia Zhai, University of Minnesota</p>
      <p>Zhi-Li Zhang, University of Minnesota</p>
    </div>
  </div>
</div>

<div style="text-align: center; margin-top: 3rem; padding-top: 2rem; border-top: 1px solid #eee;">
  <p>&copy; 2025 free5GC World Forum. All rights reserved.</p>
</div>
