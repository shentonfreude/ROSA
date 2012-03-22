=========
 Reports
=========

Reports come from a remote system, rana.hq.nasa.gov:8080/businessobjects/enterprise115/rosa/viewrpt....

excel: http://rana.hq.nasa.gov:8080/businessobjects/enterprise115/rosa/viewrpt.csp

pdf: http://rana.hq.nasa.gov:8080/businessobjects/enterprise115/rosa/viewrpt.cwr

Spreadsheet output -- for all apps -- is not helpful, just formatting.

Curent App report takes a long time. The URL is also insecure as it's not HTTPS like ROSA

Reports
=======

* Application Pipeline (Abbreviated) -- requires date range
* Application Pipeline (Full) -- requires date range
* Current Production Releases
* All Current and In Development Releases by Acronym
* Total Current Apps/Web Sites and Releases In Development (core and 10.x)
* Types of Current Production Appliations by Acronym: ugly bar chart x=code, y=#: c/s+web, c/s, webapp
* Production Web Sites by Organization Acronym: bar chart like previous, not so ugly
* MOnthly Analysis of Applications Released: trend analysis: feb2012 is blank
* Software Releases, Core vs. Non-Core: bar chart x=core/noncore/total, y=#

Examples
========

Current and In Development
--------------------------

Headers:

* application category
* software class
* acronym
* system name
* verion 
* status
* relase date
* task order
* org acronym
* nasa requester
* SR#

Current App: PAVE
-----------------
::
  PAVE
  Application
  Application Name Application Description
  Application Owner Application Functional Type NASA Analyst
  Software Class
  Release/Configuration
  Release Status
  Version Number
  Version Change Description
  Release Date SR Number
  Security/Compliance
  System Type
  BIA Information Category Information Sensitivity Authentication Method Personal ID Info Indicator Personal ID Data Type Compliance - 2810 Compliance - 508 Compliance - AWRS
  Organizational/Support Team
  Organizational Title Organization Acronym NASA SR Requestor Task Order
  Triage Level
  Support - Branch Manager Support - Project Manager Support - Primary Developer Support - Alternate Developer
  Usage/Frequency
  Application User Group Frequency Used Number of Users
  Architecture
  Architecture Type
  URL
  Supporting DBMS
  Supporting Software
  Supporting Server - Application Supporting Server - Database Supporting Server - Report Supporting Network Services Used
  Version :
  Project Announcement Visibility Effort
  Enables NASA personnel to advertise projects to targeted staff or everyone.
  Rhonda HortonTaylor General Admin Liteshia Dennis
  F
  Current Version
  2.5.3
  Update the scheduled task that pulls the emails from HQTS.
  2/23/2012 2012-2001663
  General Support System Low
  Other
  ID/PW and Token
  No
  NOT APPLICABLE Yes
  Yes
  Yes
  HQ Human Resources Mgmt Div LM040
  Rhonda Horton-taylor
  10.01
  Call List
  Arvo Hall
  Tanya Hamlet
  Ryan Stewart-Frederick Marithe Le
  Agency-Wide Monthly
  383
  Web App https://smith.hq.nasa.gov/pave Oracle 10g
  Oracle 10g ColdFusion 8 Smith
  Wesson
  Not Applicable
  Extranet
  2.5.3
  Interface/Shared Dependencies
  Application Interface Acronym HQTS,WIMS Application Interface Direction Pull,Pull Appication Interface Method Auto,Auto Federal Records Qualification Yes
  NRRS Disposition Yes NRRS Schedule/Item 3/12

Current App: HQTS
-----------------
::
  HQTS
  Application
  Application Name Application Description
  Application Owner Application Functional Type NASA Analyst
  Software Class
  Release/Configuration
  Release Status
  Version Number
  Version Change Description
  Release Date SR Number
  Security/Compliance
  System Type
  BIA Information Category Information Sensitivity Authentication Method Personal ID Info Indicator Personal ID Data Type Compliance - 2810 Compliance - 508 Compliance - AWRS
  Organizational/Support Team
  Organizational Title Organization Acronym NASA SR Requestor Task Order
  Triage Level
  Support - Branch Manager Support - Project Manager Support - Primary Developer Support - Alternate Developer
  Usage/Frequency
  Application User Group Frequency Used Number of Users
  Architecture
  Architecture Type
  URL
  Supporting DBMS
  Supporting Software
  Supporting Server - Application Supporting Server - Database Supporting Server - Report Supporting Network Services Used
  Version : 3.6
  Headquarters Transformation Solution
  Provides HQ custom applications with a standardized way to access personnel directory information by using web services.
  LITESHIA B DENNIS General Admin Liteshia Dennis
  G
  In Development
  3.6
  Please implement the HQTS Failover capability. The solution to be implemented will be based on recommendations made in the Service Request 2011 ?0001425 'HQTS Failover Whitepaper' submitted by HITSS. Further discussions with ITCD will be required to decide on the specific solution to be implemented. HITSS will provide a cost estimate to include labor and ODC's required to support the implemented solution.
  4/19/2012 2011-0001649
  General Support System Low
  Public-by request only Not Applicable
  No
  Not Applicable Not Applicable Not Applicable Yes
  HQ Info Tech & Communications Div LM020
  LITESHIA B DENNIS
  10.01
  Call List
  Arvo Hall
  Tanya Hamlet Dawayne Pretlor ANTHONY WILLIAMS
  HQ-Wide DAILY
  9
  Web App
  https://ws.hq.nasa.gov/hqts/NasaDirectory.cfc?wsdl
  ORACLE 10G
  Sun ONE Web Server, XML/DSML, NDC,COLDFUSION MX 8 SMITH
  WESSON
  Not Applicable
  Extranet
  Interface/Shared Dependencies
  Application Interface Acronym Application Interface Direction Appication Interface Method Federal Records Qualification NRRS Disposition
  NRRS Schedule/Item
  HATS;HPSS;HQeD;ICET;MBPD;NED;PAVE;FOCUS;PFSS;SEEL;NVDB;CICO;SWLDB;X500-BS;NEST Push;Push;Push;Push;Push;Pull;Push;Push;Push;Push;Push;Push;Push;Push;Push Auto;Auto;Auto;Auto;Auto;Auto;Auto;Auto;Auto;Auto;Auto;Manual;Auto;Auto;Auto
  No
  No
  NOT APPLICABLE
