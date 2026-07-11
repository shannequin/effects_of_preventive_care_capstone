ANALYSIS_CONFIG = {
    'Colorectal': {
        'Description': 'Colorectal cancer screenings include colonoscopy, sigmoidoscopy, virtual colonoscopy, CT colonography, blood stool test, FIT DNA, or Cologuard test.',
        'Screenings': ['hadsigm4', 'colncncr', 'vircolo1', 'smalstol', 'stooldn2'],
        'Analysis': {
            'Insurance Type': {
                'indicator': 'primins2',
                'base_category': 'No coverage of any type',
                'header': 'Is primary insurance type significantly associated with the likelihood of receiving colorectal cancer screening?'
            },
            'Income Level': {
                'indicator': 'income3',
                'base_category': 'Less than $10,000',
                'header': 'Is income level significantly associated with the likelihood of receiving colorectal cancer screening?'
            },
            'Sex': {
                'indicator': 'sex3',
                'base_category': 'Female',
                'header': 'Is sex significantly associated with the likelihood of receiving colorectal cancer screening?'
            },
            'Education Level': {
                'indicator': 'educa',
                'base_category': 'Never attended school or only kindergarten',
                'header': 'Is education level significantly associated with the likelihood of receiving colorectal cancer screening?'
            }
        }
    },
    'Womens Wellness': {
        'Description': 'Womens wellness screenings include breast and cervix screenings.',
        'Screenings': ['hadmam', 'cervscrn'],
        'Analysis': {
            'Insurance Type': {
                'indicator': 'primins2',
                'base_category': 'No coverage of any type',
            'header': 'Is primary insurance type significantly associated with the likelihood of receiving womens wellness screening?'
            },
            'Income Level': {
                'indicator': 'income3',
                'base_category': 'Less than $10,000',
                'header': 'Is income level significantly associated with the likelihood of receiving womens wellness screening?'
            },
            'Marital Status': {
                'indicator': 'marital',
                'base_category': 'Never married',
                'header': 'Is marital status significantly associated with the likelihood of receiving womens wellness screening?'
            },
            'Education Level': {
                'indicator': 'educa',
                'base_category': 'Never attended school or only kindergarten',
                'header': 'Is education level significantly associated with the likelihood of receiving womens wellness screening?'
            }
        }
    }
}