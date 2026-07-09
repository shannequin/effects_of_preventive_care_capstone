# Data Science Capstone Requirements

**Project Summary**

The capstone project is an opportunity for you to showcase the skills you learned throughout
the bootcamp by designing, executing, and presenting an individually crafted project. The
challenge of completing a project that has not been pre-defined enables you to stretch your
analytical, technical, and organization skills. The end result of this effort will be a presentation that enables you to communicate the findings of your analysis. This project will serve as the keystone of your portfolio. The instructor’s involvement is to support progress and arrival at an MVP defined by the student. This includes ensuring students meet deadlines, support and troubleshoot student efforts toward data acquisition, analysis, visualization, or presentation, regular check-ins and feedback with students, and preparation for demo day.

**Data Selection and Preparation**

* Determine an area of personal or professional interest that you would like to explore
with data.
* The data you work with should enable you to demonstrate your proficiency in cleaning, merging, and preparing data for analysis.
* The dataset should also enable you to answer three to four data questions so you can showcase your analytical abilities.
* Ideally, the project should involve either multiple datasets or one sufficiently complex dataset that requires extensive cleaning, integration, data preparation, or involves the use of APIs or web scraping techniques.
* The primary dataset cannot be sourced from Kaggle or used in previous class projects.
* While proprietary data may be used with prior instructor approval, your data cannot contain Personally Identifiable Information (PII) visible in the final deliverables.

**Data Questions**

* Formulate appropriately scoped and sufficiently complex data question(s) to guide your project.
* Maintaining a clear focus on the data question(s) throughout the project, will ensure all data collection, preparation, analysis, and visualizations are aligned with answering them effectively.
* The questions should be distinct from those explored in previous class projects.
* You are not required to include machine learning or natural language processing in your capstone.

**GitHub Requirements**

* You will need to maintain an organized and well-documented codebase on GitHub.
* You should make at least one commit per class session to show regular progress.
* As you are wrapping up your project, you should include a demonstration of the analysis process, showcasing the steps taken to arrive at the final results.
* You should include an informative and representative README file that provides an overview of the project, instructions for running the code, and details on the chosen technologies and techniques.
* Ensure there is no visible PII in the code or final deliverables.
* The exception to the aforementioned requirements if projects using proprietary data. In this case, communicate with your instructor about how to make your code assemble for review.

**Capstone Presentation**

* As your capstone presentation is used to share your project on Demo Day, the presentation must effectively communicate your project's findings using relevant visualizations that meaningfully contribute to your audience's understanding of your findings. Your presentation must be  ontained in PowerPoint, an interactive dashboard, or another appropriate and approved medium.
* In order to participate in demo day and graduate, you must demonstrate your completed capstone project to the instructor and obtain approval by the end of your final class session.

**Capstone Support**

* Seek regular support and troubleshooting from your instructor throughout the project, especially in areas related to data acquisition, analysis, visualization, and presentation.
* Maintain regular check-ins and feedback sessions with the instructor to receive guidance and ensure progress aligns with the Minimum Viable Product (MVP) defined by the student.

# Project Proposal

**Executive Summary**
This section provides an overview of the project. It should briefly touch on the motivation, data question, data to be used, along with any known assumptions and challenges.

*I am passionate about preventative healthcare like cancer screenings and vaccines. I want to know how quality of life and death rates are affected by preventative care. I am interested in data about health screenings, vaccines, and deaths. I assume males and lower income areas take less prevention measures.*

**Motivation**

Here you will go into more detail about why you have chosen this project.

*Many people needlessly die due to undiagnosed issues that could have been resolved by prevention or early detection. Not only is it important to make the decision to go to the doctor, but for many people, that decision is made for them due to it being financially prohibiting.*

**Data Question**

Present your question. Feel free to include any research/articles that are relevant or show where others have attempted to answer this question.

*How does preventative healthcare affect quality of life and death rates?*

# Notes

* Create Google Doc for documenting the process: https://docs.google.com/document/d/1v-E5yx_0U507c50uh5mUwsKBTDiMeami7YytXxGiHFA/edit?usp=sharing
* Create conda environment yaml file: *conda env export > environment.yml*
* Create pip requirements file: *pip list --format=freeze > requirements.txt*
* Create .env file for environment variables
* Set Python interpreter to conda
* Set project to Python search path: *set PYTHONPATH=C:\Users\shann\Documents\NSS\effects_of_preventive_care_capstone*
* Run locally: *streamlit run src/app.py*