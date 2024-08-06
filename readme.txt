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
