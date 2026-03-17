The eval agent uses this rubric: [Archie the Agent Rubric](https://docs.google.com/document/d/16o0yQ7SNs33w7xg4EbE6BGAKXPsdllRXLTp74Dz1NSY/edit?tab=t.0)  
Details of the eval agent and Archie can be found here: [Archie Instructions](https://docs.google.com/document/d/16ZobDOOndN3WDR-gmlXWuaAsGLaCwXDwzb2NByM0A70/edit?tab=t.8b1bzqyhxzlr) [Archie's Evaluator Instructions](https://docs.google.com/document/d/1500xiMtK68NkuoSDkUaU1u0EsaHqO4iBYObsXQU57Ug/edit?tab=t.0)

| Prompt \# | Prompt | My Score | Evaluation Agent Score | Notes |
| :---- | :---- | :---- | :---- | :---- |
| **1** | **Targeted question:** What were the key takeaways from the AI engineer workflows interview regarding the BYOK functionality? | 23 | 23 | The model met the basic expectation of answering a valid query without needing to engage the limitation-handling protocol.  |
| **2** | **Targeted question:** In the OpenShift Virtualization survey, what was the exact quote or finding related to rightsizing to prevent under-provisioning? | 19 | 17 | Did not create a tracing log The model met the basic expectation of answering a valid query without needing to engage the limitation-handling protocol. |
| **3** | **General question:** What have we learned about HCC OpenShift Lightspeed in the last 6 months? | 23 | 23 | The model met the basic expectation of answering a valid query without needing to engage the limitation-handling protocol. |
| **4** | **General question:** Across all studies, what are the common themes or pain points users consistently experience with onboarding into ISV Partner Managed Services? | 23 | 23 | The model met the basic expectation of answering a valid query without needing to engage the limitation-handling protocol. |
| **5** | **Out-of-Scope question:** What is the industry-standard success rate for SaaS application onboarding? | 25 | 23 | Agent deducted points because technically no data was being referenced, so nothing exceeded expectations for accuracy of data (this is not a problem in the human’s opinion) |
| **6** | **Out-of-Scope question:** What research do we have on the newly launched feature, Red Hat OpenShift Mobile Phones? | 23 | 25 | Did not scope to only UXD research studies folder but did a great job at disagreeing with the user |
| **7** | **Assumption Testing:** I have an assumption that AI Engineers prefer command-line over UI for configuring their models. What evidence do we have that supports or refutes this? | 25 | 25 | Exceeded expectations across the board |
| **8** | **Direct Quotes:** Give me 3 direct, verbatim user quotes about RHEL Lightspeed frustrations that I can use in a slide deck. | 21 | 19 | Lost most of its points because it only gave the quotes without any context for those quotes. |
| **9** | **Methodology Check:** Was the data regarding Product360 gathered via a survey (quant) or interviews (qual)? | 25 | 23 |  |
| **10** | **Methodology Check:** What kind of testing has been done in the InstructLab space? | 23 | 21 | Response included an InstructLab blog post from IBM Research Japan |
| **11** | **Recency Filter:** What are the most recent findings regarding the Hybrid Cloud Console from the last 12 months? | 25 | 25 |  |
| **12** | **Contradiction Search:** I assume users love dark mode toggle buttons. Please find any research findings that contradicts this or show users struggling with it. | 21 | 21 | Several references to outside context |
| **13** | **Dead End Check:** What are the top 3 questions about Red Hat OpenShift AI that our current research *cannot* answer? | 25 | 25 |  |
| **14** | **Broad Synthesis:** I am new to the Hybrid Cloud Console. Summarize the top 3 user goals and top 3 user pain points I should be aware of. | 21 | 21 | Several references to outside context |
| **15** | **Feature Validation:** Did any users specifically request an AI model comparison feature in the last year of interviews? | 25 | 25 |  |
| **AVG** | **AVG** | 23.13 | 22.6 |  |

