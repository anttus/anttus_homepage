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
      misc: {},
      about: { texts: [] },
      experience: { header: "", jobs: [] },
      education: { header: "", education: [] },
      certifications: { header: "", data: [] },
      projects: { header: "", data: [] },
      skills: { header: "", skills: [] },
    },

    init() {
      this.fetchGistCV();

      window.addEventListener("popstate", (event) => {
        this.showCV = !!(event.state && event.state.page === "cv");
      });

      if (window.location.hash === "#cv") {
        this.showCV = true;
      }
    },

    openCV() {
      this.showCV = true;
      // Push history state so the Back button works
      if (window.location.hash !== "#cv") {
        history.pushState({ page: "cv" }, "", "#cv");
      }
    },

    closeCV() {
      this.showCV = false;
      // Push history state to revert URL back to home root
      if (window.location.hash === "#cv") {
        history.pushState({ page: "home" }, "", window.location.pathname);
      }
    },

    fetchGistCV() {
      // Only set loading UI if user clicked CV before prefetch finished
      if (this.showCV && !this.fetched) {
        this.loading = true;
      }

      this.error = false;
      const GIST_URL =
        "https://api.github.com/gists/d1285d208ef1cb4d54e27561251e38cd";

      fetch(GIST_URL)
        .then((res) => {
          if (!res.ok) throw new Error(`HTTP Error ${res.status}`);
          return res.json();
        })
        .then((payload) => {
          let rawJsonString = "";

          if (payload && payload.files && typeof payload.files === "object") {
            const fileKeys = Object.keys(payload.files);
            if (fileKeys.length === 0)
              throw new Error("No files found in Gist.");
            rawJsonString = payload.files[fileKeys[0]].content;
          } else {
            throw new Error("Invalid Gist structure.");
          }

          this.data = JSON.parse(rawJsonString);
          this.fetched = true;
        })
        .catch((err) => {
          console.error("Fetch error:", err);
          this.error = true;
          this.errorMessage = err.message;
        })
        .finally(() => {
          this.loading = false;
        });
    },
  };
}
