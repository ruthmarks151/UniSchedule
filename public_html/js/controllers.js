TimTab.controller('TitleCtrl',['$scope','ServicePack',function($scope, Services){
    $scope.title = function(){
        return Services.title()
    }
}])

