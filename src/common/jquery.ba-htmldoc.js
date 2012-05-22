/*!
 * jQuery htmlDoc "fixer" - v0.2pre - 12/15/2010
 * http://benalman.com/projects/jquery-misc-plugins/
 * 
 * Copyright (c) 2010 "Cowboy" Ben Alman
 * Dual licensed under the MIT and GPL licenses.
 * http://benalman.com/about/license/
 */

(function($){
  
  var // RegExp that matches opening and closing HTML, HEAD, BODY tags.
      // $1 = slash, $2 = tag name, $3 = attributes
      rtag = /<(\/?)(html|head|body)(\s+[^>]*)?>/ig,
      
      // Unique id prefix for selecting placeholder elements.
      prefix = 'hd' + +new Date();
  
  $.htmlDoc = function( str ) {
    var // A collection of "intended" elements that can't be rendered
        // cross-browser with .innerHTML, for which placeholders must be
        // swapped.
        elems = $([]),
        
        // Input HTML string, parsed to include placeholder DIVs.
        parsed,
        
        // A node under which a temporary DOM tree can be constructed.
        root;
    
    // Replace HTML, HEAD, BODY tags with DIV placeholders.
    parsed = str.replace( rtag, function( tag, slash, name, attrs ) {
      
      var // Current intended / placeholder element index.
          len = elems.length,
          
          // Temporary object in which to hold attributes.
          obj = {};
      
      // If this is an opening tag...
      if ( !slash ) {
        
        // Add an element of this name into the collection of elements. Note
        // that if a string of attributes is added at this point, it fails.
        elems = elems.add( '<' + name + '/>' );
        
        // If the original tag had attributes, create a temporary div with
        // those attributes. Then, copy each attribute from the temporary div
        // over to the temporary object.
        if ( attrs ) {
          $.each( $( '<div' + attrs + '/>' )[0].attributes, function(i,v){
            obj[ v.name ] = v.value;
          });
        }
        
        // Set the attributes of the intended object based on the attributes
        // copied in the previous step.
        elems.eq( len ).attr( obj );
      }
      
      // A placeholder div with a unique id replaces the intended element's
      // tag in the parsed HTML string.
      return '<' + slash + 'div'
        + ( slash ? '' : ' id="' + prefix + len + '"' ) + '>';
    });
    
    // If placeholder elements were necessary...
    if ( elems.length ) {
      
      // Create the root node and append the parsed, place-held HTML.
      root = $('<div/>').html( parsed );
      
      // Replace each placeholder element with its intended element.
      $.each( elems, function(i,v){
        var elem = root.find( '#' + prefix + i ).before( elems[i] );
        elems.eq(i).html( elem.contents() );
        elem.remove();
      });
      
      // Return the topmost intended element(s), sans text nodes.
      return root.children();
    }
    
    // No placeholder elements were necessary, so just return a normal
    // jQuery-parsed HTML string.
    return $(str);
  };
  
})(jQuery);
