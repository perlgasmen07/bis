College
+------Buildings
	+------Floor
		+------Rooms

+----------------------Tables---------------------+
+------College
    +------ID
    +------shortname
    +------description
    +------inserted_by
    +------updated_by
    +------created_at
    +------updated_at  

+------Buildings
    +------ID
    +------shortname
	+------college_id
    +------inserted_by
    +------updated_by
    +------created_at
    +------updated_at
    
+------BuildingAttribute
    +------ID
    +------building_id
    +------attribute_id
    +------inserted_by
    +------updated_by
    +------created_at
    +------updated_at    

            
+------Attributes
    +------ID
    +------shortname 
    +------value
    +------has_property
    +------inserted_by
    +------updated_by
    +------created_at
    +------updated_at       
        +------examples
            +------No. of Floors (no property) datatype: int
            +------Building footprint (sqm) (no property) datatype: int
            +------Total floor Area (sqm) (no property) datatype: int
            +------Building Conditions (has property)
                +------renovated areas (in the last 10 years) datatype: int
                +------on-going renovations datatype: boolean yes/no
                +------for future renovation (TFA - (Renovated+On-going))   datatype: int 
            +------Projected Renovation Cost datatype: int
            +------Structural Requirement (has property)
            +------Repainting (no property) datatype: boolean yes/no
            +------Pwd Requirements (has property)
            +------Gender_Neutral_CR (no property) datatype: boolean yes/no
            +------permits_availability (has property)
            +------Utilities (has property)
            +------ecc_requirements (has property)

+------AttributeProperty
    +------ID
    +------building_id
    +------attribute_id
    +------inserted_by
    +------updated_by
    +------created_at
    +------updated_at

+------Properties
    +------ID
    +------shortname
    +------value
    +------inserted_by
    +------updated_by
    +------created_at
    +------updated_at
        +------examples
            +------renovated areas (in the last 10 years) datatype: int
            +------on-going renovations datatype: boolean yes/no
            +------for future renovation (TFA - (Renovated+On-going))   datatype: int     
            +------Cost/sqm datatype: int
            +------Proposed Development Cost for Future Renovations datatype: int   
            +------Structural Integrity Assessment datatype: boolean yes/no
            +------Retrofitting + date datatype: boolean and date  
            +------Ramp datatype: boolean yes/no + string
            +------Elevator datatype: boolean yes/no + string
            +------PWD Rest Room datatype: boolean yes/no + string
            +------Buillding Permit (date issued) datatype: boolean yes/no + string storage_path
            +------Occupancy Permit (date issued)datatype: boolean yes/no + string storage_path 
            +------Generator datatype: boolean yes/no + string storage_path
            +------Cistern datatype: boolean yes/no + string storage_path
            +------Septic tank datatype: boolean yes/no + string storage_path
            +------Upgraded Electrical Wiring datatype: boolean yes/no + string storage_path
            +------Upgraded Electrical Connection LVSG datatype: boolean yes/no + string storage_path
            +------FDAS datatype: boolean yes/no + string storage_path
            +------Fire Protection System datatype: boolean yes/no + string storage_path
            +------Ventilation datatype: boolean yes/no + string storage_path
            +------Fiber Optics/Structured Cabling/LAN datatype: boolean yes/no + string storage_path
            +------CMR Submission datatype: boolean yes/no + string storage_path
            +------SMR Submission datatype: boolean yes/no + string storage_path
            +------Testing requirements datatype: boolean yes/no + string storage_path

+------Floor
    +------ID
    +------Level(shortname)
    +------building_id
    +------no. of Rooms
    +------inserted_by
    +------updated_by
    +------created_at
    +------updated_at

+------Rooms
    +------ID
    +------Room Number
    +------floor_id
    +------inserted_by
    +------updated_by
    +------created_at
    +------updated_at

+------Roles
    +------ID
    +------Name
            +------CPDMO Staff
                +------View building data
                +------Building attribute data entry
            +------CPDMO Chief
                +------View Building data
                +------Generate Report
                    +------export all
                    +------export selected attributes
                +------Generate Analysis
            +------System Administrator
                +------User CRUD
                +------College CRUD
                +------Building CRUD
                +------Floor CRUD
                +------Room CRUD
                +------Add categories for attributes for Buildings
                +------Add more attributes for Buildings
    +------inserted_by
    +------updated_by
    +------created_at
    +------updated_at
    
+------Users
    +------ID
    +------Name
    +------role_id
    +------inserted_by
    +------updated_by
    +------created_at
    +------updated_at

+----------------------Tasks---------------------+
+------Database Migrations + Seeders
+------Roles Model
+------User Crud
+------GoogleAuth Login
+------Require Login for pages
+------for System Administrator
    +------College CRUD
    +------Building CRUD
    +------Floor CRUD
    +------Room CRUD
+------report Generation