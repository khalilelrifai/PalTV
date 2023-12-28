$(function() {
    function moveProgressBar() {
        // Animate the progress bar from 0% to 100%
        $(".progress-wrapper .progress-bar").animate({ height: "100%" }, 3000, function() {
            // Reset the progress bar to 0% when the animation is complete
            $(this).css("height", "0%");
            // Recursively call the function to create an infinite loop
            moveProgressBar();
        });
    }

    // Call the function to start the infinite loop
    moveProgressBar();
});