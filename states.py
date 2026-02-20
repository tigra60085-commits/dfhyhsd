# Conversation states
(
    MAIN_MENU,
    # Drug browsing
    DRUG_CLASS_SELECT,
    DRUG_LIST,
    DRUG_INFO,
    DRUG_DETAIL,
    # Quiz
    QUIZ_MENU,
    QUIZ_CATEGORY,
    QUIZ_DIFFICULTY,
    QUIZ_QUESTION,
    QUIZ_NEXT,
    # Flashcards
    FLASHCARD_CATEGORY,
    FLASHCARD_SHOW,
    FLASHCARD_RATE,
    # Clinical cases
    CASE_LIST,
    CASE_READ,
    CASE_QUESTION,
    CASE_ANSWER,
    # Interactions
    INTER_DRUG1,
    INTER_DRUG2,
    INTER_RESULT,
    # Search
    SEARCH_INPUT,
    SEARCH_RESULT,
    # Misc screens
    NT_SELECT,
    GLOSSARY_BROWSE,
    PROGRESS_VIEW,
    TIP_VIEW,
    COMPARE_SELECT1,
    COMPARE_SELECT2,
    # Pharma-compare (detailed drug comparison)
    PHARMA_COMPARE_INPUT,
    PHARMA_COMPARE_CONTEXT,
    PHARMA_COMPARE_FOCUS,
    PHARMA_COMPARE_AUDIENCE,
    # Podcast dialog generator
    PODCAST_TOPIC,
    PODCAST_CASE,
    PODCAST_DURATION,
    # Clinical case formatter (case-format skill)
    CASE_FORMAT_INPUT,
    CASE_FORMAT_FOCUS,
    CASE_FORMAT_OPTIONS,
    # Dose calculator
    DOSE_CALC_DRUG,
    DOSE_CALC_RESULT,
    # Monitoring guide
    MONITOR_DRUG,
    MONITOR_RESULT,
    # Scale calculator
    SCALE_SELECT,
    SCALE_INPUT,
    SCALE_RESULT,
    # Pregnancy & lactation safety
    PREG_DRUG,
    PREG_RESULT,
    # Withdrawal / tapering guide
    WITHDRAW_DRUG,
    WITHDRAW_RESULT,
) = range(50)
