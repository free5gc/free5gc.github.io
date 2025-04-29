<!-- <iframe width="616" height="400" src="https://www.youtube.com/embed/SFO2z5-4zxs?list=PLeDUIabcS2_p4fjApgJHNiVpfYSzz1oJi" title="free5GC Demonstration with 5G SA gNB and UE" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe> -->

<!-- Google tag (gtag.js) --> <script async src="https://www.googletagmanager.com/gtag/js?id=G-JETJ7TJ805"></script> <script> window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag('js', new Date()); gtag('config', 'G-JETJ7TJ805'); </script>

<div class="hero-container">
  <div class="hero-content">
    <img width="300" src="./assets/logo.png" alt="free5GC Logo" class="hero-logo"/>
    <h1 class="hero-title">Open Source 5G Core Network Implementation</h1>
    <p class="hero-description">free5GC is a Linux Foundation project dedicated to implementing 3GPP Release 15 and beyond 5G core networks</p>
    <div class="hero-buttons">
      <a href="https://github.com/free5gc/free5gc" class="hero-button primary" target="_blank">Get Started</a>
      <a href="./guide/contribute/" class="hero-button secondary">How to Contribute</a>
    </div>
  </div>
</div>

<div class="announcement-box">
  <h2>The 1st free5GC World Forum 2025 Call For Papers</h2>
  <p>We are excited to announce the 1st free5GC World Forum 2025, which will be held in Taipei, Taiwan, October 13, 2025. This event aims to bring together researchers, developers, and industry professionals to share their insights and advancements in the field of 5G core networks.</p>
  <p>For more details, please visit the <a href="https://www.free5gc.org/forum/" target="_blank">forum website</a>.</p>
  <h2>Latest News: free5GC v4.0.1 Released!</h2>
  <p>We have fixed a series of bugs in version 4.0.1 to improve stability.</p>
  <p>For more details, please see the hisory page.</p>
  <a href="./history" class="announcement-link">View Version History →</a>
</div>

<div class="features-container">
  <div class="feature-card">
    <div class="feature-icon">📱</div>
    <h3>Complete 5G Core Implementation</h3>
    <p>Compliant with 3GPP R15+ standards, providing comprehensive 5G core network functionalities</p>
  </div>
  <div class="feature-card">
    <div class="feature-icon">🌐</div>
    <h3>Service-Based Architecture</h3>
    <p>Built on Service-Based Architecture (SBA) for modular and scalable deployments</p>
  </div>
  <div class="feature-card">
    <div class="feature-icon">🚀</div>
    <h3>Containerized Deployment</h3>
    <p>Supports Kubernetes and Docker deployments, easily integrating with modern cloud-native environments</p>
  </div>
  <div class="feature-card highlighted">
    <div class="feature-icon">🔓</div>
    <h3>Open Source</h3>
    <p>Licensed under Apache 2.0, free for both commercial and non-commercial use with no restrictions</p>
  </div>
</div>

The free5GC (a Linux Foundation project) is an open-source project for 5th generation (5G) mobile core networks. The ultimate goal of this project is to implement the 5G core network (5GC) defined in 3GPP Release 15 (R15) and beyond.

Currently, the major contributors are from National Yang Ming Chiao Tung University ([NYCU](https://en.nycu.edu.tw/){target=_blank}).

- The source code of the latest version of free5GC can be downloaded from [here](https://github.com/free5gc/free5gc){target=_blank}.
- Information about TSC (Technical Steering Committee) can be found at [free5gc/governance](https://github.com/free5gc/governance/blob/main/CONTRIBUTORS.md).
- Follow our [LinkedIn](https://www.linkedin.com/company/free5gc/){target=_blank} page to get the news about free5GC.
- Please refer to our roadmap for the features of each release.

> [!NOTE]
> - The Linux Foundation announced that free5GC officially joined the Linux Foundation on September 16, 2024, during the Open Source Summit Europe in Vienna, Austria. Check out the press release [here](https://www.linuxfoundation.org/press/worlds-leading-open-source-mobile-packet-core-free5gc-moves-under-linux-foundation-to-provide-open-source-alternatives-across-5g-deployments).
> - Please check out the [Google Scholar](https://scholar.google.com/scholar?hl=en&as_sdt=2007&q=free5gc) page here for publications using free5GC.

### Connecting to the Future!

<div class="roadmap-container">
  <img src="./assets/roadmap-202503.png" alt="free5GC Roadmap" class="roadmap-image"/>
  <div class="roadmap-text">
    <p>We remain committed to enhancing free5GC with new features, and we have a roadmap in place to support the following functionalities:</p>
    <ul class="roadmap-list">
      <li>NR-DC</li>
      <li>Roaming</li>
    </ul>
    <a href="#" class="roadmap-button">Learn More About free5GC Development Plans</a>
  </div>
</div>

<style>
  .hero-container {
    background: linear-gradient(135deg, #0b5394 0%, #073763 100%);
    color: white;
    padding: 3rem 2rem;
    margin: 0 -1.5rem 2rem -1.5rem;
    border-radius: 8px;
    text-align: center;
  }
  
  .hero-logo {
    margin-bottom: 1rem;
  }
  
  .hero-title {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    font-weight: bold !important;
    color: white !important;
  }
  
  .hero-description {
    font-size: 1.2rem;
    max-width: 800px;
    margin: 0 auto 2rem auto;
  }
  
  .hero-buttons {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 1.5rem;
  }
  
  .hero-button {
    padding: 0.8rem 1.5rem;
    border-radius: 4px;
    font-weight: bold;
    text-decoration: none;
    transition: all 0.3s ease;
  }
  
  .hero-button.primary {
    background-color: #ffffff;
    color: #0b5394;
  }
  
  .hero-button.primary:hover {
    background-color: #f0f0f0;
    transform: translateY(-2px);
  }
  
  .hero-button.secondary {
    border: 2px solid white;
    color: white;
  }
  
  .hero-button.secondary:hover {
    background-color: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
  }
  
  .features-container {
    display: flex;
    flex-wrap: wrap;
    gap: 1.5rem;
    justify-content: center;
    margin: 3rem 0;
  }
  
  .feature-card {
    background-color: #f8f9fa;
    border-radius: 8px;
    padding: 1.5rem;
    width: calc(33% - 1rem);
    min-width: 250px;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }
  
  .feature-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
  }
  
  .feature-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
  }
  
  .feature-card.highlighted {
    background-color: #f0f7ff;
    border: 1px solid #b3d7ff;
  }
  
  .announcement-box {
    background-color: #e6f7ff;
    border-left: 4px solid #1890ff;
    padding: 1.5rem;
    margin: 2rem 0;
    border-radius: 0 8px 8px 0;
  }
  
  .announcement-box h2 {
    color: #0b5394;
    margin-top: 0;
  }
  
  .announcement-link {
    display: inline-block;
    margin-top: 1rem;
    color: #1890ff;
    font-weight: bold;
    text-decoration: none;
  }
  
  .roadmap-container {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 2rem;
    margin: 2rem 0;
    background-color: #f8f9fa;
    padding: 2rem;
    border-radius: 8px;
  }
  
  .roadmap-image {
    max-width: 100%;
    flex: 1;
    min-width: 300px;
  }
  
  .roadmap-text {
    flex: 1;
    min-width: 300px;
  }
  
  .roadmap-list {
    margin: 1rem 0;
    padding-left: 1.5rem;
  }
  
  .roadmap-button {
    display: inline-block;
    background-color: #0b5394;
    color: white !important;
    padding: 0.7rem 1.2rem;
    border-radius: 4px;
    text-decoration: none;
    margin-top: 1rem;
    transition: background-color 0.3s ease;
  }
  
  .roadmap-button:hover {
    background-color: #073763;
  }
  
  @media (max-width: 768px) {
    .hero-title {
      font-size: 2rem;
    }
    
    .feature-card {
      width: 100%;
    }
    
    .roadmap-container {
      flex-direction: column;
    }
  }
</style>
