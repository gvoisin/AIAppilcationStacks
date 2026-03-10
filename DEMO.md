## Demo queries

This file includes different options to test out the LLM and Agent applications alone or side by side, highlighting the difference and main strengths of each application.

### Stand alone *LLM application*

1. Relational DB queries:
    - Which work orders are still open and their associated asset types?
    - List assets that are currently in overwatch condition (condition_score < 4)
    - Show circuits with their substation names and total customers served, ordered by customer count
    - Find outages that lasted more than 2 hours and their associated root cause assets
2. RAG queries:
    - What are the EPA recommended actions for power outages in the US?
    - What immediate steps should be taken during a widespread power outage according to US guidelines?
    - Summarize key communication protocols from disaster response manuals during outages
3. DB + RAG queries (mixed):
    - Look for the outages in residential areas, and then explain, what recovery procedures does the disaster manual recommend?
    - Compare average outage duration by cause category and reference relevant EPA guidelines

### Stand alone *Agent application*

1. Graph DB queries:
    - Show me all substations and their capacity in descending order (low)
    - Visualize substation locations with capacity indicators
    - Display asset health distribution by condition score, include names if possible.
2. RAG queries:
    - How do disaster response manuals address communication during outages?
    - Create a timeline visualization of FEMA assistance steps for electrical outages
3. DB + RAG queries (mixed):
    - Map outage locations and overlay EPA recommended response zones
    - Generate a dashboard showing work order priorities with referenced manual safety protocols

### Side by side comparison

1. Relational DB queries:
    - What are the most common outage cause categories in the last 6 months?
    - Find circuits with the highest number of customers served
2. RAG queries:
    - What are the EPA recommended actions for power outages in the US?
    - What immediate steps should be taken during a widespread power outage according to US guidelines?
3. DB + RAG queries (mixed):
    - Compare outage resolution times for circuits originating from different substations, and what the disaster manual says about response times
    - Analyze customer complaints by outage category and correlate with FEMA assistance guidelines
    - Show asset maintenance schedules alongside safety protocol requirements from manuals

### Queries to test
b. RAG-only queries:
   6. What are the EPA recommended actions for power outages in the US?
   7. How does FEMA assist with electrical outages?
   8. What procedures are outlined in the Mexican disaster manual for infrastructure recovery?
   9. What immediate steps should be taken during a widespread power outage according to US guidelines?
   10. How do disaster response manuals address communication during outages?
c. Mixed queries:
   11. For outages caused by assets in poor condition, what EPA actions are recommended?
   12. How should work orders be prioritized for assets that serve customers in critical infrastructure?
   13. What FEMA procedures apply to outages affecting commercial customers during weather events?
   14. Compare outage resolution times for circuits originating from different substations, and what the disaster manual says about response times
   15. For assets requiring maintenance in the next 30 days, what safety protocols from the manuals should be followed?