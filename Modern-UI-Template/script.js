document.addEventListener("DOMContentLoaded", () => {
  // Mobile menu toggle with enhanced animations
  const mobileMenuButton = document.querySelector(".mobile-menu-button")
  const mobileNav = document.querySelector(".mobile-nav")
  const mobileMenuIcon = mobileMenuButton.querySelector("i")

  // Intersection Observer for section animations
  const sectionObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = "1"
          entry.target.style.transform = "translateY(0)"
          sectionObserver.unobserve(entry.target)
        }
      })
    },
    {
      threshold: 0.2,
      rootMargin: "50px",
    }
  )

  // Observe all sections
  document.querySelectorAll("section").forEach((section) => {
    section.style.opacity = "0"
    section.style.transform = "translateY(30px)"
    section.style.transition = "all 0.8s cubic-bezier(0.16, 1, 0.3, 1)"
    sectionObserver.observe(section)
  })

  mobileMenuButton.addEventListener("click", () => {
    mobileNav.classList.toggle("active")
    mobileMenuIcon.classList.toggle("fa-bars")
    mobileMenuIcon.classList.toggle("fa-times")
    mobileMenuButton.style.transform = mobileNav.classList.contains("active") ? "rotate(90deg)" : "rotate(0deg)"
    mobileMenuButton.style.transition = "transform 0.4s cubic-bezier(0.16, 1, 0.3, 1)"
    
    // Enhanced mobile nav animation
    if (mobileNav.classList.contains("active")) {
      mobileNav.style.transform = "translateY(0)"
      mobileNav.style.opacity = "1"
    } else {
      mobileNav.style.transform = "translateY(-10px)"
      mobileNav.style.opacity = "0"
    }
  })

  // Close mobile menu when clicking on a link
  const mobileNavLinks = document.querySelectorAll(".mobile-nav .nav-link")
  mobileNavLinks.forEach((link) => {
    link.addEventListener("click", () => {
      mobileNav.classList.remove("active")
    })
  })

  // Enhanced FAQ accordion functionality with smooth animations
  const faqItems = document.querySelectorAll(".faq-item")

  faqItems.forEach((item) => {
    const question = item.querySelector(".faq-question")
    const answer = item.querySelector(".faq-answer")

    // Set initial styles
    answer.style.maxHeight = "0"
    answer.style.opacity = "0"
    answer.style.transition = "all 0.5s cubic-bezier(0.16, 1, 0.3, 1)"

    question.addEventListener("click", () => {
      const isActive = item.classList.contains("active")

      // Close all other items with animation
      faqItems.forEach((otherItem) => {
        if (otherItem !== item && otherItem.classList.contains("active")) {
          const otherAnswer = otherItem.querySelector(".faq-answer")
          otherAnswer.style.maxHeight = "0"
          otherAnswer.style.opacity = "0"
          otherItem.classList.remove("active")
        }
      })

      // Toggle current item with enhanced animation
      if (!isActive) {
        item.classList.add("active")
        answer.style.maxHeight = `${answer.scrollHeight}px`
        answer.style.opacity = "1"
      } else {
        item.classList.remove("active")
        answer.style.maxHeight = "0"
        answer.style.opacity = "0"
      }
    })
  })

  // Enhanced smooth scrolling for anchor links with progress indicator
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      if (this.getAttribute("href") !== "#") {
        e.preventDefault()

        const targetId = this.getAttribute("href")
        const targetElement = document.querySelector(targetId)

        if (targetElement) {
          const startPosition = window.pageYOffset
          const targetPosition = targetElement.offsetTop - 80
          const distance = targetPosition - startPosition
          const duration = 1000
          let start = null

          function animation(currentTime) {
            if (start === null) start = currentTime
            const timeElapsed = currentTime - start
            const progress = Math.min(timeElapsed / duration, 1)

            const easeInOutCubic = progress < 0.5
              ? 4 * progress * progress * progress
              : 1 - Math.pow(-2 * progress + 2, 3) / 2

            window.scrollTo(0, startPosition + distance * easeInOutCubic)

            if (timeElapsed < duration) {
              requestAnimationFrame(animation)
            }
          }

          requestAnimationFrame(animation)
        }
      }
    })
  })

  // Form URL replacement
  const formLinks = document.querySelectorAll('a[href="https://forms.google.com/your-form-url"]')
  // Replace with your actual Google Form URL
  const actualFormUrl = "https://forms.google.com/your-form-url"

  formLinks.forEach((link) => {
    link.setAttribute("href", actualFormUrl)
  })

  // Email replacement
  const emailLinks = document.querySelectorAll('a[href="mailto:info@carteleriapro.com"]')
  // Replace with your actual email
  const actualEmail = "info@carteleriapro.com"

  emailLinks.forEach((link) => {
    link.setAttribute("href", `mailto:${actualEmail}`)
  })
})