function initRest()
{
	if ($('.crumb.category').text().length > 0 && $('.crumb.section').text().length > 0){

		var lat = undefined;
		var lon = undefined;
		if ($.trim($('.crumb.category').text()) == "free stuff" &&
			$.trim($('.crumb.section').text()).indexOf("for sale") > -1) {

    		$(".postinginfos").append('<p class="postinginfo">\
    			<button class="reply_button js-only">Buy With Postmates<span class="envelope">&#9993;</span> <span class="phone">&#9742;</span></button><span class="replylink"><a id="replylink" href="/reply/stl/zip/4851207787">reply</a></span></p>')
       		//grab yahoo address heh
    		var link = $($(".mapaddress").find("small").find("a")[1]).attr("href")
    		if (link != undefined) {
    			getParameters = link.split("#")[1].split("&")
	    		for (var i=1; i < getParameters.length; i++) {
	    			params = getParameters[i].split("=");
	    			if (params.length > 1 && params[0] == "lat") {
	    				lat = params[1];
	    			} else if  (params.length > 1 && params[0] == "lon") {
	    				lon = params[1];
	    			}
	    		}
    		}
    		
		}
		$(".userbody").append('<div class="injected-dialog">\
								<p class="texto">Get a Quote from Free For Free</p>\
									<div class="injected-form"><form id="injected" method="post">\
										<span class="fontawesome-user"></span><input id="add1" type="text"  placeholder="Address Line 1">\
										<span class="fontawesome-user"></span><input id="add2" type="text"  placeholder="Address Line 2">\
										<span class="fontawesome-user"></span><input id="city" type="text"  placeholder="City">\
										<span class="fontawesome-user"></span><input id="state" type="text"  placeholder="State">\
										<span class="fontawesome-user"></span><input id="zip" type="text"  placeholder="Zip">\
										<input type="hidden" id="destLat"><input type="hidden" id="destLong">\
										<input type="submit" value="Get Quote">\
									</form></div>');
		$("#destLat").val(lat);
		$("#destLong").val(lon);

		$("#injected").submit(function(event) {
			event.preventDefault();
			addressArray = [$("#add1").val(), $("#add2").val(), $("#city").val(), $("#state").val(), $("#zip").val()];
			console.log(addressArray.join(" "));
			$.post( "http://pavleen.me/getquote", {"destination_address": addressArray.join(" "),
							"destLat": lat,
							"destLon": lon})
			  .done(function( data ) {
			    var price = (parseInt(data["fee"])/100);
			    $(".injected-dialog").remove()
			    $(".userbody").append('<div class="injected-form"><p class="texto">Estimated Price: $' + price.toFixed(2) + '<p>\
			    									<form id="injected-next" method="post">\
			    									<span class="fontawesome-user"></span><input id="buyer_name" type="text"  placeholder="Name">\
			    									<span class="fontawesome-user"></span><input id="buyer_email" type="text"  placeholder="Email">\
													<span class="fontawesome-user"></span><input id="dropoff_notes" type="text"  placeholder="Notes for drop off">\
													<span class="fontawesome-user"></span><input id="dropoff_phone_number" type="text"  placeholder="Phone Number">\
													<input type="hidden" id="item_name"><input type="hidden" id="dropoff_address"><input type="hidden" id="seller_email"><input type="hidden" id="quote_id">\
													<input type="submit" value="Buy Now">\
			    									</form></div>');
			    $('.reply_button.js-only').trigger('click');
			    $("#item_name").val($.trim($(".postingtitle").text()));
			    $("#dropoff_address").val(data['dropoff_address']);
			    $("#quote_id").val(data["id"]);


			    //setTimeout(function() {$("#seller_email").val($.trim($(".anonemail").text()));},500);
			    $("#seller_email").val("pav920@gmail.com");
		    	$("#injected-next").submit(function(event) {
					event.preventDefault();
					vals = $("#injected-next :input");
					params = {};
					for (var i=0; i < vals.length; i++) {
						console.log(vals[i]);
						params[vals[i]["id"]] = vals[i].value;
					}
					console.log(params);
				    $.post( "http://pavleen.me/sendpurchase", params)
						.done(function( data ) {
							console.log(data);
					});
				});

			});
		});
		

	}
}
initRest();