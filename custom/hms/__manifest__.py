{
    'name' : 'HMS',
    'description' : 'Hospital mangement system',
    "depends": ["base", "crm"],
    'data': [
        "security/hms_groups.xml",
        "security/ir_rule.xml",
        "security/ir.model.access.csv",
        "views/hms_actions.xml",
        "views/hms_menus.xml",
        'views/hms_patient_views.xml',
        'views/hms_department_views.xml',
        'views/hms_doctors_views.xml',
         "reports/report_patient_template.xml",
        "reports/report.xml",
    ],

}
