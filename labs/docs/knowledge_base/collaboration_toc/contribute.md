---
title: "How to Contribute"
sidebar_position: 393
---



## Quick Method: Create an Issue

If you've found some issues or typos in the ThreeFold Manual, feel free to [create an issue on the ThreeFold Manual repository](https://github.com/threefoldtech/grid_manual/issues) to let us know. We will then be able to fix it as soon as possible.

The steps are simple:

* Go to the [issues section of ThreeFold Manual](https://github.com/threefoldtech/grid_manual/issues) repository on GitHub
* Click on `New Issue`
* Choose an appropriate title
* Explain briefly the issue you found
* Click `Submit New Issue`



## Advanced Method: Create a Pull Request

If you found an issue in the manual and you wish to fix the issue yourself, you can always fork the repository and propose the changes in a pull request. We present the main steps in this section as well as further details on how to proceed efficiently.



### Main Steps to Add Content

We present here the main steps to add content to the Threefold Manual by forking the repository [`threefoldtech/info_grid`](https://github.com/threefoldtech/grid_manual) to your own Github account.

* Go to the Threefold Manual repository: [https://github.com/threefoldtech/grid_manual](https://github.com/threefoldtech/grid_manual)
* Fork the Development branch
  * On the top right corner, click `Fork -> Create a new fork`
* Make changes in the forked repository
   * To add a new section
      * Add a new Markdown file to the appropriate directory under `docs/`
      * Update the sidebar configuration in `sidebars.js` if needed
   * To modify an existing section:
     * Make the changes directly in the Markdown file
* Test your changes locally
  * Clone your forked repository:
    ```bash
    git clone https://github.com/YOUR_GIT_ACCOUNT/info_grid
    cd info_grid
    ```
  * Install dependencies and start the development server:
    ```bash
    make dev
    ```
  * The development server will start automatically at http://localhost:3000
  * Make changes and see them live-reload in your browser
* Ask for a pull request
  * In the forked repository, click `Contribute -> Open pull request`
* Once the pull request is accepted, the changes will be available on the live site

Note: You can update your forked repository by clicking `Sync fork -> Update branch`.



### How to View the Site Locally

To view the site locally and test your changes:

1. Install dependencies and start the development server:
   ```bash
   make dev
   ```
   This will:
   - Update pricing values from external sources
   - Start the development server with live reloading
   - Open the site in your default browser at http://localhost:3000

2. To build the site for production:
   ```bash
   make build
   ```

3. To clean build artifacts:
   ```bash
   make clean
   ```
