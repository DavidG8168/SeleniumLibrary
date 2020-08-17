*** Settings ***
Library  SeleniumLibrary

*** Test Cases ***
AlertTest
    Open Browser    https://www.w3schools.com/html/html_iframe.asp    firefox
    get webelement  //*[@id="main"]/div[3]/iframe
    frame should contain   //*[@id="main"]/div[3]/iframe     html
    execute javascript  return 5;
    element should contain  //*[@id="main"]/h1/span     Iframes
    mouse over  //*[@id="main"]/h1/span
    mouse out   //*[@id="main"]/h1/span
    click element at coordinates  //*[@id="main"]/h1/span   100    100
    page should contain element     //*[@id="main"]/h1/span
    locator should match x times    //*[@id="main"]/h1/span     1
    set window size     400     400
    Close Browser