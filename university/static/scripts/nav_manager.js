function register_button(
    button,  // element
    managing_block,  // element
    other_buttons,  // array of other button elements
    other_blocks  // array of other block elements
) {
    button.addEventListener(
        "click",
        function() {
            button.style.color = "#ffffff"
            managing_block.style.display = "grid"
    
            for (var i = 0; i < other_buttons.length; i++) {
                other_buttons[i].style.color = "#464954"
                other_blocks[i].style.display = "none"
            }
        }
    )

    button.addEventListener(
        "mouseover",
        function() {
            if (managing_block.style.display == "none")
                button.style.color = "#7a55ff"
        }
    )

    button.addEventListener(
        "mouseleave",
        function() {
            if (managing_block.style.display == "none")
                button.style.color = "#464954"
        }
    )
}
