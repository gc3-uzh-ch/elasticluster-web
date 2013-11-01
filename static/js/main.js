/**
 * Client logic to control the start cluster form.
 * @param $scope dependency injection see angularjs doc
 * @param $http dependency injection see angularjs doc
 * @param $templateCache dependency injection see angularjs doc
 * @constructor
 */
function StartClusterCtrl($scope, $http, $templateCache) {
    $scope.invalid_cloud_cred = false;
    $scope.advanced_optoins = false;


    /**
     * Checks if the user stored any credentials for the selected
     * cloud provider. If there are no credentials found, a message
     * will be shown.
     */
    $scope.update_cloud_provider = function(){
        var id = $scope.form.cloud_provider
        if (id != null && id.length != 0){
            $http.post('/start/cloud/check', {'id': id}, $templateCache)
                .success(function(data, status){
                    console.log(data)
                    if(data.user_cloud.length == 0){
                        $scope.invalid_cloud_cred = true;
                    }

                    if(data.cloud_service){
                        var cloud = data.cloud_service[0].fields;
                        $scope.form.image = cloud.default_image;
                        $scope.form.flavor = cloud.default_flavor;
                        $scope.form.security_group = cloud.default_security_group;
                        $scope.form.image_user = cloud.default_image_user;
                    }
                }
             );
        }
        $scope.invalid_cloud_cred = false;
    };

    /**
     * Opens the modal to enter credentials for the cloud provider.
     */
    $scope.enter_cloud_credentials = function(){
        $scope.cred_form.ec2_access_key = "";
        $scope.cred_form.ec2_secret_key = "";
        var modal = jQuery('#credentials_modal');
        modal.modal({
            onShow: function(){
                if($scope.form.cloud_provider){
                    // todo: this value is only set, if the modal was rendered once at least. Should work for first time as well.
                    jQuery('#id_cloud_service').val($scope.form.cloud_provider);
                }
            }
        }).modal('toggle')
    };

    /**
     * Sends an ajax request to store the cloud provider credentials and checks.
     * The message to enter cloud credentials will disappear after this action.
     */
    $scope.submit_cloud_credentials = function(){
        if($scope.cred_form.$valid){
            event.preventDefault(); // this prevents the page from sending the form
            $http.post('/start/cloud/cred/' + $scope.cred_form.cloud_service, $scope.cred_form, $templateCache)
                .success(function(data, status){
                    console.log(data)
                    $scope.update_cloud_provider();
                    var modal = jQuery('#credentials_modal');
                    modal.modal('hide');
                })
        }
    }


    /**
     * When the user selects a cluster, this will send a request to the server in order to get the
     * options about the nodes in the cluster.
     */
    $scope.cluster_update = function(){
        if($scope.form.cluster){
            $http.get("/start/cloud/cluster_type/" + $scope.form.cluster).success(function(data, status){
                $scope.form.nodes = data;
            })
        } else{
            $scope.form.nodes = null;
        }
    };

}



/**
 * Initialises dropdowns (this is needed by semantic-ui).
 */
jQuery(document).ready(function(){
    jQuery('.ui.dropdown')
        .dropdown()
    ;
})




/**
 * AngularJS module initialisation
 *  - sets the template notation to {[]} to not conflict with the django template notation
 *  - renames the header and cookie name to meet the change csrf implementation
 */
angular.module('elasticluster-web', []).config(function($interpolateProvider, $httpProvider){
        // change angular notation symbol to not conflict django template language
        $interpolateProvider.startSymbol('{[').endSymbol(']}');

        // django csrf implementation compatibility
        $httpProvider.defaults.xsrfCookieName = 'csrftoken';
        $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

        // Use x-www-form-urlencoded tontent-type, so django will recognize data and render it to request.POST
        $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';

        // Override $http service's default transformRequest
        // to enable ajax request to pass the object instead of a serialized version (e.g. jQuery('form').serialize())
        $httpProvider.defaults.transformRequest = [function(data)
        {
            /**
             * The workhorse; converts an object to x-www-form-urlencoded serialization.
             * @param {Object} obj
             * @return {String}
             */
            var param = function(obj)
            {
                var query = '';
                var name, value, fullSubName, subName, subValue, innerObj, i;

                for(name in obj)
                {
                    value = obj[name];

                    if(value instanceof Array)
                    {
                        for(i=0; i<value.length; ++i)
                        {
                            subValue = value[i];
                            fullSubName = name + '[' + i + ']';
                            innerObj = {};
                            innerObj[fullSubName] = subValue;
                            query += param(innerObj) + '&';
                        }
                    }
                    else if(value instanceof Object)
                    {
                        for(subName in value)
                        {
                            subValue = value[subName];
                            fullSubName = name + '[' + subName + ']';
                            innerObj = {};
                            innerObj[fullSubName] = subValue;
                            query += param(innerObj) + '&';
                        }
                    }
                    else if(value !== undefined && value !== null)
                    {
                        query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
                    }
                }

                return query.length ? query.substr(0, query.length - 1) : query;
            };

            return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
        }];
    }
);




/**
 * Adjust jQuery to send the csrf cookie with every ajax request.
 * (see https://docs.djangoproject.com/en/dev/ref/contrib/csrf/#ajax)
**/
jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});