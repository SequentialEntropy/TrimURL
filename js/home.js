const homebutton = document.getElementById("homebutton");
const aboutbutton = document.getElementById("aboutbutton");
const trimbutton = document.getElementById("trimbutton");
const contactbutton = document.getElementById("contactbutton");

const homesection = document.getElementById("title");
const aboutsection = document.getElementById("about");
const trimsection = document.getElementById("trim");
const contactsection = document.getElementById("contact");

const navbar = document.getElementById("navbar");

const currenturl = document.getElementsByClassName("currenturl");
for (i = 0; i < currenturl.length; i++) {
    currenturl[i].textContent = window.location.host + "/";
}

const scrollerrormargin = 3;

function removeactive() {
    homebutton.classList.remove("active");
    aboutbutton.classList.remove("active");
    trimbutton.classList.remove("active");
    contactbutton.classList.remove("active");
}

function gettop(element) {
    var top = 0;

    while (element.tagName != "BODY") {
        top += element.offsetTop;
        element = element.offsetParent;
    }

    return top;
}

function getbuttonstop() {
    hometop = gettop(homesection);
    abouttop = gettop(aboutsection);
    trimtop = gettop(trimsection);
    contacttop = gettop(contactsection);
}

//Debouncer

var latestKnownScrollY = 0,
    ticking = false;

function onScroll() {
    latestKnownScrollY = window.scrollY;
    requestTick();
}

function requestTick() {
    if (!ticking) {
        requestAnimationFrame(update);
    }
    ticking = true;
}

//Scroll Update

function update() {
    ticking = false;

    var currentScrollY = latestKnownScrollY;

    if (currentScrollY + scrollerrormargin < abouttop) {
        removeactive();
        homebutton.classList.add("active");
        navbar.style.height = "20vh";
    } else {
        if (currentScrollY + scrollerrormargin < trimtop) {
            removeactive();
            aboutbutton.classList.add("active");
        } else if (currentScrollY + scrollerrormargin < contacttop) {
            removeactive();
            trimbutton.classList.add("active");
        } else {
            removeactive();
            contactbutton.classList.add("active");
        }
        navbar.style.height = "12.5vh";
    }
}

function copy() {
    let copyingtext = document.getElementsByClassName("feedbacklink")[0];
    let textarea = document.createElement("textarea");
    let copybutton = document.getElementById("copy");
    textarea.value = copyingtext.textContent;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand("copy");
    textarea.remove();
    copybutton.textContent = "Copied!";
    setTimeout(function() {
        copybutton.textContent = "Copy Link"
    }, 500);
}

getbuttonstop();
window.addEventListener("scroll", onScroll, false);
window.addEventListener("resize", getbuttonstop);