$(function(e) {
	'use strict'
	
	// Select2
	$('.select2').select2({
		minimumResultsForSearch: Infinity
	});
	
	// Select2 by showing the search
	$('.select2-show-search').select2({
		minimumResultsForSearch: ''
	});
	
	// Select2 by Flag
	function formatState (state) {
	  if (!state.id) { return state.text; }
	  var $state = $(
		'<span><img src="../../assets/images/flags/' +  state.element.value.toLowerCase() +
	'.svg" class="img-flag" /> ' +
	state.text +  '</span>'
	 );
	 return $state;
	};

	$(".select2-flag-search").select2({
	  templateResult: formatState,
	  templateSelection: formatState,
	   escapeMarkup: function(m) { return m; }
	});
});