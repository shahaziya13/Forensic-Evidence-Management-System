
-- Paste your SQL CREATE TABLE and INSERT statements here
!mysql -u root -proot -e 'USE forensic_db; CREATE TABLE cases(case_id INT PRIMARY KEY, case_name VARCHAR(100), crime_type VARCHAR(100), status VARCHAR(50));'
!mysql -u root -proot -e 'USE forensic_db; CREATE TABLE investigator(investigator_id INT PRIMARY KEY, name VARCHAR(100), rank_name VARCHAR(100));'
!mysql -u root -proot -e 'USE forensic_db; CREATE TABLE evidence(evidence_id INT PRIMARY KEY, case_id INT, type VARCHAR(100), description VARCHAR(200), collected_date DATE, FOREIGN KEY(case_id) REFERENCES cases(case_id));'
!mysql -u root -proot -e 'USE forensic_db; CREATE TABLE custody(custody_id INT PRIMARY KEY, evidence_id INT, investigator_id INT, date_received DATE, FOREIGN KEY(evidence_id) REFERENCES evidence(evidence_id), FOREIGN KEY(investigator_id) REFERENCES investigator(investigator_id));'
!mysql -u root -proot -e "USE forensic_db; INSERT INTO cases VALUES (1,'Bank Robbery','Theft','Open'),(2,'City Murder','Homicide','Closed'),(3,'Cyber Fraud','Cyber Crime','Investigating'),(4,'Jewelry Theft','Burglary','Open'),(5,'Museum Artifact Theft','Artifact Smuggling','Closed');"
!mysql -u root -proot -e "USE forensic_db; INSERT INTO investigator VALUES (101,'Rahul Sharma','Inspector'),(102,'Aisha Khan','Sub Inspector'),(103,'Arjun Nair','Detective'),(104,'Sneha Reddy','Forensic Analyst'),(105,'Vikram Patel','Crime Officer');"
!mysql -u root -proot -e "USE forensic_db; INSERT INTO evidence VALUES (201,1,'Fingerprint','Fingerprint on vault','2025-01-10'),(202,2,'Knife','Knife recovered','2025-01-12'),(203,3,'Laptop','Hacked laptop','2025-01-15'),(204,4,'CCTV','Camera footage','2025-01-18'),(205,5,'Ancient Coin','Rare coin found','2025-02-02');"
!mysql -u root -proot -e "USE forensic_db; INSERT INTO custody VALUES (301,201,101,'2025-01-11'),(302,202,102,'2025-01-13'),(303,203,103,'2025-01-16'),(304,204,104,'2025-01-19'),(305,205,105,'2025-02-03');"
