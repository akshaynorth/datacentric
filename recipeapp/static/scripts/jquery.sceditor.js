/*----------------------------------------------------*/
/*  SCEditor
/*----------------------------------------------------*/

(function($){
	$(document).ready(function(){
		function addIng() {
			var newElem = $('table#ingredients-sort tr.ingredients-cont.ing:first').clone();
			newElem.find('input').val('');
			newElem.appendTo('table#ingredients-sort');
		}

		function addInstruction() {
			var newElem = $('table#instructions-sort tr.ingredients-cont.ing:first').clone();
			newElem.find('input').val('');
			newElem.appendTo('table#instructions-sort');
		}

		//sortable table
		var fixHelper =  function(e, tr) {
		    var $originals = tr.children();
		    var $helper = tr.clone();
		    $helper.children().each(function(index)
		    {
		      // Set helper cell sizes to match the original sizes
		      $(this).width($originals.eq(index).width());
		    });
		    return $helper;
		  };
		if ($("table#ingredients-sort").is('*')) {
			$('table#ingredients-sort + .add_ingredient').click(function(e){
				e.preventDefault();
				addIng();
			});

			// remove ingredient
			$('#ingredients-sort .delete').live('click',function(e){
				e.preventDefault();
				$(this).parent().parent().remove();
			});

			$('table#ingredients-sort tbody').sortable({
				forcePlaceholderSize: true,
				forceHelperSize: true,
				placeholder : 'sortableHelper',
				helper: fixHelper,
				zIndex: 999990,
				opacity: 0.6,
				tolerance: "pointer"
			});
        }
			// Adding recipe instructions
        if ($("table#instructions-sort").is('*')) {
			$('table#instructions-sort + .add_ingredient').click(function(e){
				e.preventDefault();
				addInstruction();
			});

			// remove instruction
			$('#instructions-sort .delete').live('click',function(e){
				e.preventDefault();
				$(this).parent().parent().remove();
			});

			$('table#instructions-sort tbody').sortable({
				forcePlaceholderSize: true,
				forceHelperSize: true,
				placeholder : 'sortableHelper',
				helper: fixHelper,
				zIndex: 999990,
				opacity: 0.6,
				tolerance: "pointer"
			});
	 	}
	 	})
})(this.jQuery);