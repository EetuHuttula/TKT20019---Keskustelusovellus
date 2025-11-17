*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem

*** Variables ***
${BROWSER}     Firefox
${BASE_URL}    http://127.0.0.1:5000/login
${USERNAME}   test_user
${PASSWORD}   test_password1!

*** Test Cases ***
Login Test
    Open Browser    ${BASE_URL}    ${BROWSER}
    Input Text    username    ${USERNAME}
    Input Text    password    ${PASSWORD}
    Click Element    //input[@type='submit']   # Assuming your login button is of type submit
    Sleep    2s  # Add a sleep to wait for the redirection or any flash messages to appear
    [Teardown]    Close Browser
