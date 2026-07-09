import streamlit as st

from utils.custom_visuals import rainbow_divider

def main() -> None:
    """
    Display Overview page.
    """
    st.title('Preventive Health Care', text_alignment='center')

    rainbow_divider()

    st.header('What is preventive health care?', )
    st.text(
        'Preventive health care for cancer includes actions that lower the risk of developing cancer or detect it at an early, ' \
        'more treatable stage, such as vaccinations, healthy lifestyle habits, regular screenings, and discussions with a ' \
        'healthcare provider about personal risk factors. Examples include avoiding tobacco, maintaining a healthy weight, ' \
        'receiving vaccines against HPV and hepatitis B, and recommended screening tests like mammograms, colonoscopies, and ' \
        'cervical cancer screening.'
    )
    st.text(
        'Generally, these services are covered at no cost to you when provided by an in-network medical provider. In most cases, ' \
        'you won\'t pay a copayment or coinsurance for certain preventive services like immunizations and screening tests, even ' \
        'if you haven\'t met your deductible. Coverage may vary. $0 cost isn\'t guaranteed in all cases.'
    )

    st.header('Why is it important?')
    st.text(
        'Preventive health care is important because it helps detect health issues early, when they are more treatable, and can ' \
        'prevent serious illnesses from developing. Regular check-ups, screenings, and vaccinations can improve overall health ' \
        'outcomes and reduce healthcare costs in the long run. Most importantly, it saves lives by giving people the best chance ' \
        'for successful treatment and a healthier future.'
    )
    
    st.header('Barriers to Care')
    st.text(
        'Barriers to preventive health care are the factors that make it difficult for people to receive recommended screenings ' \
        'and other preventive services. These barriers can lead to delayed diagnoses, reduced screening rates, and poorer health ' \
        'outcomes.'
    )
    st.text(
        'Barriers can include lack of awareness, limited access to healthcare services, financial constraints, and cultural ' \
        'stigmas that may discourage individuals from seeking preventive care.'
    )

if __name__ == '__main__':
    main()