define(["underscore","backbone","backboneCommon","ajaxControl","js/follow/FollowPopup"],function(f,k,b,g,l){var d=!1;return k.View.extend({tagName:"p",className:"friend",events:function(){var a={};a[b.cgti+" .wrap"]=this.detailPopup;a[b.cgti+" .followBtn"]=this.followBtn;a[b.cgti+" .supportCheckBtn"]=this.supportCheck;return a},initialize:function(b,c){this.listenTo(this.rootView,"sortRemove",this.sortHandler);this.listenTo(this.rootView,"allCheck",this.allCheck);this.listenTo(this.rootView,"collectRemove",
this.collectRemove);this.listenTo(this.rootView,"removeView",this.removeView);this.userType=c;this.userId="follow"===this.userType?this.model.followUserId:"follower"===this.userType?this.model.followerUserId:"block"===this.userType?this.model.blockUserId:"search"===this.userType?this.model.id:this.model.userId},render:function(b){this.template=f.template($("#userParts").text());this.$el.html(this.template({model:this.model}));this.model.blocked?this.el.getElementsByClassName("messageWrap")[0].textContent=
"Blocked":this.el.getElementsByClassName("messageWrap")[0].textContent=this.model.comment?this.model.comment:"";this.el.dataset.scrollHash=this.userId;return this},allCheck:function(a,c){switch(a){case "follow":"follow"!==this.userType&&this.userId===c&&(b.addClass(this.el.getElementsByClassName("followIcon")[0],"on"),this.model.follow=!0,"search"!==this.userType&&"follower"!==this.userType||this.userId!==c||b.addClass(this.el.getElementsByClassName("followBtn")[0],"already"));break;case "unfollow":"follow"===
this.userType&&this.userId===c?this.removeView():"follow"!==this.userType&&this.userId===c&&(b.removeClass(this.el.getElementsByClassName("followIcon")[0],"on"),this.model.follow=!1,"search"!==this.userType&&"follower"!==this.userType||this.userId!==c||b.removeClass(this.el.getElementsByClassName("followBtn")[0],"already"));break;case "block":"block"!==this.userType&&this.userId===c&&(b.addClass(this.el.getElementsByClassName("blockIcon")[0],"on"),this.model.blocked=!0,this.el.getElementsByClassName("messageWrap")[0].textContent=
"Blocked");break;case "unblock":"block"===this.userType&&this.userId===c?this.removeView():"block"!==this.userType&&this.userId===c&&(b.removeClass(this.el.getElementsByClassName("blockIcon")[0],"on"),this.model.blocked=!1)}},detailPopup:function(a){this.btnFlg?this.btnFlg=!1:(a.preventDefault(),b.isScrolled()||l.instantPopup(a,this.model,this.userType,this,this.rootView.pagingView.pageNum))},followBtn:function(a){a.preventDefault();if(!b.isScrolled()&&!d)if(this.btnFlg=!0,this.rootView.maxFollowCnt<=
b.storage.userFollowList.length)new b.PopupClass({title:"Too Many Follows",content:"You reached the Follow limit.\x3cbr\x3eYou cannot Follow any more Players.\x3cbr\x3e\x3cbr\x3e"+("Follows: "+b.storage.userFollowList.length+"/"+this.rootView.maxFollowCnt+""),closeBtnText:"Close"});else{d=!0;var c=this;g.ajaxPost(b.linkList.sendFollow,{friendUserId:this.userId},function(a){d=!1;if("error"!==a.resultCode){var e=b.storage.userFollowList.length+a.userFollowList.length;b.responseSetStorage(a);new b.PopupClass({title:"Add to Follows",
content:"Added \x3cspan class\x3d'c_pink'\x3e"+c.model.userName+"\x3c/span\x3e to Follows.\x3cbr\x3e\x3cbr\x3e"+("Follows: "+e+"/"+c.rootView.maxFollowCnt+""),closeBtnText:"Close"});b.addClass(c.el.getElementsByClassName("followBtn")[0],"already");c.rootView.allCheckAndChange(c.userId,"follow")}})}},supportCheck:function(a){a.preventDefault();if(!b.isScrolled()&&!d){this.btnFlg=!0;a=this.model;var c=this.userType,f=this.rootView.pagingView.pageNum,e="follow"===c?a.followUserId:"follower"===c?a.followerUserId:
"block"===c?a.blockUserId:"search"===c?a.id:a.userId,h=function(a){"error"!==a.resultCode&&(window.isLocal&&(a=JSON.parse(a)),b.supportCheckModel=a,b.followSave.active=!0,b.followSave.scrollHash=e,b.followSave.pagingNum=f,location.href="#/ProfileFormationSupport")};window.isLocal?require(["text!/magica/json/friend/user/1.json"],function(a){h(a)}):g.ajaxSimpleGet(b.linkList.followerProfile,e,h)}},sortHandler:function(){"follow"===this.userType&&(this.off(),this.remove(),delete this.model.view)},collectRemove:function(a){this.userType===
a&&(this.off(),this.remove(),delete this.model.view)},removeView:function(){this.off();this.remove();delete this.model.view}})});