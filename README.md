# Encyclopontus

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

htmx allows you to access AJAX, CSS Transitions, WebSockets and Server Sent Events directly in HTML, without having to write any JavaScript. To get started, familiarize yourself with the htmx syntax and attributes through htmx documentation:

- [htmx in a Nutshell](https://htmx.org/docs/#introduction)
- [htmx Reference](https://htmx.org/reference/)

## npm Script Tags

In the package.json file, you'll find several npm scripts defined, here's what they do:

- `tailwind` - Builds the Tailwind CSS file from the CSS source, watches for changes and rebuilds automatically.
