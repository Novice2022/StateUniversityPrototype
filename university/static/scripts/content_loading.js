function load_view(
    view_name,
    context,
    container,
    done_callback
) {
    $.post(
        view_name,
        context
    ).done(
        function(response) {
            container.innerHTML = response

            if (done_callback)
                done_callback()
        }
    ).fail(
        function(response) {
            container.innerHTML = "<h2>Can\'t load data</h2>"
        }
    )
}
