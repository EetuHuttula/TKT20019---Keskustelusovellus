*** Settings ***
Library    SeleniumLibrary
Library    OperatingSystem

*** Variables ***
${BROWSER}     Firefox
${BASE_URL}    http://127.0.0.1:5000/
${title}    title
${content}    content

*** Test Cases ***
Post Test
    Open Browser    ${BASE_URL}    ${BROWSER}
    Input Text   title    ${title}
    Input Text    content    ${content}
    Click Element    //input[@type='submit']   
    Sleep    2s  
    [Teardown]    Close Browser
