(function($){
	$(document).ready(function(){
	    function create_recipe() {
	        // Gather all the information on the generate cooking directions form
            var recipe_label = $('#recipe_label').val().trim()

            if (recipe_label.length == 0) {
                alert('Please provide a recipe label.');
                return;
            }
	        // Send a request to the flask application to create the recipe
	    }

	    $('#create_recipe_btn').click(function(e) {
	        e.preventDefault();
            create_recipe();
	    });
	})

})(this.jQuery);