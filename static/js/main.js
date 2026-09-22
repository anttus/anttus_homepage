document.addEventListener("DOMContentLoaded", function (event) {
  document.getElementById("footerText").innerHTML += new Date().getFullYear();
  setGreetingByTime();
});

function setGreetingByTime() {
  const curHours = new Date().getHours();
  const mainHeader = document.getElementById("main-header");
  if (curHours >= 0 && curHours < 5) {
    mainHeader.innerHTML = "Good night!";
  } else if (curHours >= 5 && curHours < 12) {
    mainHeader.innerHTML = "Good morning!";
  } else if (curHours >= 12 && curHours < 18) {
    mainHeader.innerHTML = "Good afternoon!";
  } else if (curHours >= 18) {
    mainHeader.innerHTML = "Good evening!";
  }
}
function siteApp() {
  return {
    showCV: false,
    loading: false,
    error: false,
    errorMessage: "",
    fetched: false,
    data: {
      info: {},
      links: {},
      about: { name: "", title: "", texts: [] },
      experience: { header: "", jobs: [] },
      education: { header: "", education: [] },
      certifications: { header: "", data: [] },
      projects: { header: "", data: [] },
      skills: { header: "", skills: [] },
    },

    init() {
      this.fetchCV();

      // Handle browser back/forward buttons
      window.addEventListener("popstate", (event) => {
        this.showCV = !!(event.state && event.state.page === "cv");
      });

      // Handle deep-linked URLs on initial load (e.g., domain.com/#cv)
      if (window.location.hash === "#cv") {
        this.showCV = true;
      }
    },

    openCV() {
      this.showCV = true;
      if (window.location.hash !== "#cv") {
        history.pushState({ page: "cv" }, "", "#cv");
      }
    },

    closeCV() {
      this.showCV = false;
      if (window.location.hash === "#cv") {
        history.pushState({ page: "home" }, "", window.location.pathname);
      }
    },

    fetchCV() {
      if (this.showCV && !this.fetched) {
        this.loading = true;
      }
      this.error = false;

      // Fetch local cached file generated during Docker build
      fetch('/static/cv-data.json')
        .then((res) => {
          if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
          return res.json();
        })
        .then((parsedJson) => {
          // Direct JSON object payload
          this.data = parsedJson;
          this.fetched = true;
        })
        .catch((err) => {
          console.error("Fetch error:", err);
          this.error = true;
          this.errorMessage = "Unable to load CV data.";
        })
        .finally(() => {
          this.loading = false;
        });
    },

    formatTitle(key) {
      const titleMap = {
        linkedin: "LinkedIn",
        github: "GitHub",
        music1: "Music",
        music2: "More music"
      };

      if (titleMap[key.toLowerCase()]) {
        return titleMap[key.toLowerCase()];
      }

      return key
        .replace(/_/g, " ")
        .replace(/\b\w/g, (char) => char.toUpperCase());
    }
  };
}
