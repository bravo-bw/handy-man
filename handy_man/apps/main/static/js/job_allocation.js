/*
 * Job Allocation script
 *
 */
/*
var job_interests = [];

class Artisan{
	constructor(job_id, artisan_id, artisan_avatar, is_best, fullname) {
	    this.job_id = job_id;
	    this.artisan_id = artisan_id;
	    this.artisan_avatar = artisan_avatar;
	    this.is_best = is_best;
	    this.fullname = fullname;
	}
}

function addJobArtisan(job_id, artisan_id, artisan_avatar, is_best, fullname){
	var artisan = Artisan(job_id, artisan_id, artisan_avatar, is_best, fullname);
	job_interests.push(artisan);
};

function job_interests_list(job_id){
	var job_interests_list = [];
	for (i=0; i<=job_interests.length; i++)
	{
		var artisan = job_interests[i];
		if (artisan.job_id == job_id){
			job_interests_list.push(artisan);
		}
	}
	return job_interests_list;
};

function best_artisan(job_id){
	var job_interests_list = job_interests_list(job_id);
	var artisan;
	for (i=0; i<=job_interests_list.length; i++)
	{
		if (job_interests[i].is_best == true){
			artisan = job_interests[i];
			break;
		}
	}
	return artisan;
};*/

$(document).ready(function (){
	function wrapRadioElements(artisan_id){ //
		$("[id='"+artisan_id+"']").wrapAll('<label name="lbl'+artisan_id+'" style="width:100%"></label>');
	}//End wrapRadioElements
	function wrapLabels(artisan_id){
		$("[name='lbl"+artisan_id+"']").wrap(
				'<div  class="radio" style="display:inline;" class="container" name="radio'+artisan_id+'"></div>');
	}
	function wrapLabelContainer(artisan_id){
		$("[name='radio"+artisan_id+"']").wrap(
				"<div id='{{identifier}}' style='background:#eee; width:100%;margin-left:1px;' class='row' name='side_nav_main'></div>");
	}//End wrapLabels
	function createRadio(artisan_id){
		$("#artisan_container").append(
				'<input type="radio" id="'+artisan_id+'" name="radio_img" value="setsiba">');
	}//End createRadio
	function createImage(artisan_id, avatar){
		$("#artisan_container").append('<img name="radio_img" id="'+artisan_id+'" alt="Artisan Image">');
		img_config = {
			'class':'img-circle',
			'width':'50',
			'height':'50',
			'src':avatar
		}
		$("img[id='"+artisan_id+"']").attr(img_config);
	}//End createImage
	function get_artisans(e, job_id){
		console.log("function get_artisans(e, job_id)");
		e.preventDefault();
		$.ajax({
			type:'GET',
			url:'/jobs/job_allocation/',
			data:{
				name:job_id,
			},
			success:function(data){
				var artisans = JSON.stringify(data);
				alert()
				$.each(data, function(idx, artisan){

				});
//				for(i=0; i<data.length; i++){
//					artisan = artisans[i];
//					create_artisan_elements(artisan);
//				}
			}
		});
	}//End get_artisans
	
	function tastypie_fetch_data(){
		$.ajax({
  		url: 'http://localhost:8000/api/v1/user/1/',
  		type: 'GET',
  		accepts: 'application/json',
  		dataType: 'json'
		});
	}
	function create_artisan_elements(artisan){
		createImage(artisan.artisan_id, artisan.avatar);
		createRadio(artisan.artisan_id);
		wrapRadioElements(artisan.artisan_id);
		wrapLabels(artisan.artisan_id);
		wrapLabelContainer(artisan.artisan_id);
		$("#artisan_container").append('<hr>');

	}// End create_artisan_elements
});
