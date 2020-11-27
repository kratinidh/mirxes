
//On loading page, activate startTab function
window.onload = function () {
  startTab();
};

//Upon loading page, default click on first tab of each sections
function startTab() {
  document.getElementsByClassName("tablinks")[0].click();
  document.getElementsByClassName("tablinks1")[0].click();
  document.getElementsByClassName("tablinks2")[0].click();
  document.getElementsByClassName("tablinks3")[0].click();
  document.getElementsByClassName("tablinks4")[0].click();
  document.getElementsByClassName("tablinks5")[0].click();
  document.getElementsByClassName("tablinks6")[0].click();
  document.getElementsByClassName("tablinks7")[0].click();
  document.getElementsByClassName("tablinks8")[0].click();
  document.getElementsByClassName("tablinks9")[0].click();
  document.getElementsByClassName("tablinks10")[0].click();
  
}

//Create tabs for tables
function openCity(evt, cityName, classOfTabContent, classOfTabLink) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName(classOfTabContent);
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName(classOfTabLink);
  for (i = 0; i < tabcontent.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", " ");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}


function generalTab(evt, cityName, classOfTabContent, classOfTabLink) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName(classOfTabContent);
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName(classOfTabLink);
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementByClassName(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}

