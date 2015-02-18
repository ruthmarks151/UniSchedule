TimTab.factory('ServicePack',['$location', function(location){
    return {
        title: function(){
            return location.url()
        }
    }
}])