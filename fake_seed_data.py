



# INSERT INTO users (email, username, first_name, last_name, location, password_hash, about_me, member_since, last_seen, active, private)
# VALUES ("email1@gmail.com", "jordanrowland", "Jordan", "Rowland", "Los Angeles, CA", "$2b$12$xO3td3LN3KExhbteQN12F.UHEI/2sVSMM4GAuRNY.LVMjlJGX2kBO", "Software Engineer", "2023-04-01", "2023-04-01", 1, 0),
# ("crazymonkey78@hotmail.com", "Starlight96", "Lily", "Jameson", "Arkania City", "$2b$12$xO3td3LN3KExhbteQN12F.UHEI/2sVSMM4GAuRNY.LVMjlJGX2kBO", "Social Media Strategist", "2023-04-01", "2023-04-01", 1, 0),
# ("pinkunicorn22@gmail.com", "PixelPenguin", "Ethan", "Chen", "Solstice City", "$2b$12$xO3td3LN3KExhbteQN12F.UHEI/2sVSMM4GAuRNY.LVMjlJGX2kBO", "Sustainability Coordinator", "2023-04-01", "2023-04-01", 1, 0),
# ("flyingeagle99@yahoo.com", "RainbowDreams", "Sophia", "Rodriguez", "New Cimmeria", "$2b$12$xO3td3LN3KExhbteQN12F.UHEI/2sVSMM4GAuRNY.LVMjlJGX2kBO", "Digital Content Creator", "2023-04-01", "2023-04-01", 1, 0),
# ("jazzsinger65@outlook.com", "Wildfire87", "Alex", "Flores", "Neo-Tokyo", "$2b$12$xO3td3LN3KExhbteQN12F.UHEI/2sVSMM4GAuRNY.LVMjlJGX2kBO", "Human Resources Analyst", "2023-04-01", "2023-04-01", 1, 0),
# ("blackpanther47@gmail.com", "LunarLioness", "Ava", "Patel", "New Arrakis", "$2b$12$xO3td3LN3KExhbteQN12F.UHEI/2sVSMM4GAuRNY.LVMjlJGX2kBO", "Customer Experience Manager", "2023-04-01", "2023-04-01", 1, 0),
# ("moonwalker86@yahoo.com", "OceanBreeze", "Michaela", "Campbell", "Cloud City", "$2b$12$xO3td3LN3KExhbteQN12F.UHEI/2sVSMM4GAuRNY.LVMjlJGX2kBO", "Brand Ambassador", "2023-04-01", "2023-04-01", 1, 0),
# ("bluejaguar33@hotmail.com", "ElectricFox", "Kai", "Williams", "Nexus City", "$2b$12$xO3td3LN3KExhbteQN12F.UHEI/2sVSMM4GAuRNY.LVMjlJGX2kBO", "Sales Operations Coordinator", "2023-04-01", "2023-04-01", 1, 0),
# ("mountainlion55@outlook.com", "MysticMoose", "Cameron", "Lee", "Zalem", "$2b$12$xO3td3LN3KExhbteQN12F.UHEI/2sVSMM4GAuRNY.LVMjlJGX2kBO", "Quality Assurance Specialist", "2023-04-01", "2023-04-01", 1, 0),
# ("happydolphin44@gmail.com", "MountainMama", "Sierra", "Ortiz", "Proxima City", "$2b$12$xO3td3LN3KExhbteQN12F.UHEI/2sVSMM4GAuRNY.LVMjlJGX2kBO", "Information Security Consultant", "2023-04-01", "2023-04-01", 1, 0),
# ("redfox21@yahoo.com", "CosmicCat", "Isaac", "Kim", "Zion", "$2b$12$xO3td3LN3KExhbteQN12F.UHEI/2sVSMM4GAuRNY.LVMjlJGX2kBO", "Logistics Coordinator", "2023-04-01", "2023-04-01", 1, 0);



data = (
    ("crazymonkey78@hotmail.com", "Starlight96", "Lily", "Jameson", "Social Media Strategist", "Arkania City"),
    ("pinkunicorn22@gmail.com", "PixelPenguin", "Ethan", "Chen", "Sustainability Coordinator", "Solstice City"),
    ("flyingeagle99@yahoo.com", "RainbowDreams", "Sophia", "Rodriguez", "Digital Content Creator", "New Cimmeria"),
    ("jazzsinger65@outlook.com", "Wildfire87", "Alex", "Flores", "Human Resources Analyst", "Neo-Tokyo"),
    ("blackpanther47@gmail.com", "LunarLioness", "Ava", "Patel", "Customer Experience Manager", "New Arrakis"),
    ("moonwalker86@yahoo.com", "OceanBreeze", "Michaela", "Campbell", "Brand Ambassador", "Cloud City"),
    ("bluejaguar33@hotmail.com", "ElectricFox", "Kai", "Williams", "Sales Operations Coordinator", "Nexus City"),
    ("mountainlion55@outlook.com", "MysticMoose", "Cameron", "Lee", "Quality Assurance Specialist", "Zalem"),
    ("happydolphin44@gmail.com", "MountainMama", "Sierra", "Ortiz", "Information Security Consultant", "Proxima City"),
    ("redfox21@yahoo.com", "CosmicCat", "Isaac", "Kim", "Logistics Coordinator", "Zion"),
)


for email, username, first_name, last_name, about_me, city in data:
    print(f'("{email}", "{username}", "{first_name}", "{last_name}", "{city}", "$2b$12$xO3td3LN3KExhbteQN12F.UHEI/2sVSMM4GAuRNY.LVMjlJGX2kBO", "{about_me}", "2023-04-01", "2023-04-01", 1, 0),')







