# Encyclopontus

This is an extremely lightweight and simplistic setup for a personal wiki a.k.a. "Digital Garden", using barebone HTML, htmx, and Tailwind/CSS. GitHub Pages serves the site as static content only, and automatically deploys on pushes to `master`.

Most source files are just HTML. The most interesting part is the <a href="https://github.com/bondii/Encyclopontus/blob/master/index.html">`index.html`</a> file in this root directory, in which the menu as well as some custom JavaScript for URL routing is defined.

## Installation

```sh
npm install
```

## Running the Application

`npm run server`

## Building and Watching Tailwind CSS

Tailwind CSS is a utility-first CSS framework that allows for highly customizable designs with low-level utility classes. The input file for Tailwind CSS can be found at `/src/styles.css`.

You can build the Tailwind CSS using this npm script:

```sh
npm run tailwind:build
```

To automatically rebuild the CSS file during development, use:

```sh
npm run tailwind
```

New to Tailwind? You're going to love it! Start reading here: [Tailwind CSS - Utility-First Fundamentals](https://tailwindcss.com/docs/utility-first)

## htmx

Never heard of it? Don't worry, it's super easy and in my opinion intuitive.
htmx allows you to access AJAX, CSS Transitions, WebSockets and Server Sent Events directly in HTML, without having to write any JavaScript. To get started, familiarize yourself with the htmx syntax and attributes through htmx documentation:

- [htmx in a Nutshell](https://htmx.org/docs/#introduction)
- [htmx Reference](https://htmx.org/reference/)

Now, to be completely fair and transparent I will warn you that I am using an unnecessarily complicated way of loading the content of the pages as a simple way of handling URL routing when deploying the site with GitHub Pages. It shouldn't be that difficult to figure out just looking in the <a href="https://github.com/bondii/Encyclopontus/blob/master/index.html">`index.html`</a> anyways, but if anything is unclear feel free to ask me and I'll happily try to explain.
