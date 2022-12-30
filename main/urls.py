from django import contrib
from django.urls import path,re_path
from . import views

urlpatterns = [
    re_path(r'^$',views.Index,name='index'),
    re_path(r'^Dashboard$',views.Dashboard,name='dashboard'),
    re_path(r'^DashboardUser$',views.DashboardUser,name='dashboard_user'),

    re_path(r'^AgreeAdmin$',views.AgreeAdmin,name='agree_admin'),

    re_path(r'^BlogList/$',views.StoreListView,name='store-list'),
    re_path(r'^BlogCreate/$',views.StoreCreateView,name='store_create'),
    re_path(r'^BlogDetails/$',views.StoreDetailsView,name='store-details'),
    re_path(r'^(?P<pk>\d+)/BlogEdit/$',views.StoreEditView,name='store-edit'),

    re_path(r'^(?P<pk>\d+)/CategoryCreate/$',views.CategoryCreateView,name='category-create'),
    re_path(r'^CategoryList/$',views.CategoryListView,name='category-list'),
    re_path(r'^(?P<pk>\d+)/CategoryEdit/$',views.CategoryEditView,name='category-edit'),
    re_path(r'^(?P<pk>\d+)/CategoryDelete/$',views.CategoryDeleteView,name='category-delete'),

    re_path(r'^(?P<pk>\d+)/(?P<store_id>\d+)/SubCategoryCreate$',views.SubCategoryCreateView,name='subcategory-create'),
    re_path(r'^SubCategoryList$',views.SubCategoryListView,name='subcategory-list'),
    re_path(r'^(?P<pk>\d+)/SubCategoryEdit$',views.SubCategoryEditView,name='subcategory-edit'),
    re_path(r'^(?P<pk>\d+)/SubCategoryDelete$',views.SubCategoryDeleteView,name='subcategory-delete'),

    re_path(r'^(?P<pk>\d+)/(?P<store_id>\d+)/SubsCategoryCreate$',views.SubsCategoryCreateView,name='subscategory-create'),
    re_path(r'^(?P<pk>\d+)/SubsCategoryEdit$',views.SubsCategoryEditView,name='subscategory-edit'),
    re_path(r'^(?P<pk>\d+)/SubsCategoryDelete$',views.SubsCategoryDeleteView,name='subscategory-delete'),
    re_path(r'^SubsCategoryList$',views.SubsCategoryListView,name='subscategory-list'),

    re_path(r'^(?P<pk>\d+)/PostCreate$',views.ProductCreateView,name='product-create'),
    re_path(r'^PostList$',views.ProductListView,name='product-list'),
    re_path(r'^(?P<pk>\d+)/PostEdit$',views.ProductEditView,name='product-edit'),
    re_path(r'^(?P<pk>\d+)/PostDelete$',views.ProductDeleteView,name='product-delete'),
    path('ajax/load-subcategorys/', views.load_subcategorys, name='ajax_load_subcategorys'),
    path('ajax/load-subscategorys/', views.load_subscaegorys, name='ajax_load_subscategorys'),

    re_path(r'^PostListBlog/(?P<pk>\d+)$',views.ProductListStoreView,name='product-list-store'),
    re_path(r'^PostDetailsBlog/(?P<pk>\d+)/(?P<store_id>\d+)/(?P<slug>[\S-]+)$',views.ProductDetailsStoreView,name='product-details-store'),

    re_path(r'^PostDetailsStore/(?P<pk>\d+)/(?P<store_id>\d+)/(?P<slug>[\S-]+)$',views.AddProductDetailsStoreView,name='add-product-details-store'),
    
    re_path(r'^(?P<pk>\d+)/PostListOrders$',views.ProductListOrdersView,name='product-list-orders'),
    re_path(r'^(?P<pk>\d+)/(?P<store_id>\d+)/(?P<slug>[\S-]+)/ProductDeleteOrder$',views.ProductDeleteOrderView,name='product-delete-order'),

    re_path(r'^(?P<pk>\d+)/ShoppingCreate$',views.ShoppingCreateView,name='shopping_create'),

    re_path(r'^(?P<pk>\d+)/ShoppingListUserOrders$',views.ShoppingListUserOrdersView,name='shopping_list_user_orders'),
    re_path(r'^(?P<pk>\d+)/(?P<order_id>\d+)/ShoppingDetailsUserOrder$',views.ShoppingDetailsUserOrderView,name='shopping_details_user_order'),

    re_path(r'^(?P<pk>\d+)/ShoppingDetailsUserOrderAdmin$',views.ShoppingDetailsUserOrderAdminView,name='shopping_details_user_order_admin'),

    re_path(r'^(?P<pk>\d+)/ShoppingDetailsUserOrderUser$',views.ShoppingDetailsUserOrderUserView,name='shopping_details_user_order_user'),

    re_path(r'^ListPost$',views.ListStoreView,name='list_store'),

    re_path(r'^(?P<pk>\d+)/OrderListUser$',views.OrderListUserView,name='order_list_user'),

    re_path(r'^(?P<pk>\d+)/(?P<store_id>\d+)/PostCategoryBlog/(?P<slug>[\S-]+)$',views.ProductCategoryStoreView,name='product_category_store'),
    re_path(r'^(?P<pk>\d+)/(?P<store_id>\d+)/PostubCategoryBlog/(?P<slug>[\S-]+)$',views.ProductSubCategoryStoreView,name='product_subcategory_store'),
    re_path(r'^(?P<pk>\d+)/(?P<store_id>\d+)/PostSubsCategoryBlog/(?P<slug>[\S-]+)$',views.ProductSubsCategoryStoreView,name='product_subscategory_store'),

    re_path(r'^(?P<pk>\d+)/OrderListUserMe$',views.OrderListUserMeView,name='order_list_user_me'),

    re_path(r'^AdminDashboard$',views.AdminDashboard,name='admin_dashboard'),
    re_path(r'^TemplateCreate$',views.TemplateCreateView,name='template_create'),
    re_path(r'^TemplateList$',views.TemplateListView,name='template_list'),
    re_path(r'^BlogListConfirmed$',views.ConfirmedStoreView,name='confirmed_store_list'),
    re_path(r'^(?P<pk>\d+)/BlogEditConfirmed$',views.ConfirmedEditStoreView,name='confirmed_store_edit'),
    re_path(r'^PostListConfirmed$',views.ConfirmedProductView,name='confirmed_product_list'),
    re_path(r'^(?P<pk>\d+)/PostEditConfirmed$',views.ConfirmedEditProductView,name='confirmed_product_edit'),

    re_path(r'^TemplateCard$',views.TemplateCardView,name='template_card'),
    re_path(r'^(?P<pk>\d+)/TemplateDetails$',views.TemplateDetailsView,name='template_details'),

    re_path(r'^ReviewList$',views.ReviewListView,name='review_list'),
    re_path(r'^(?P<pk>\d+)/ReviewDelete$',views.ReviewDeleteView,name='review_delete'),

    re_path(r'^UserList$',views.UserListView,name='user_list'),

    re_path(r'^(?P<pk>\d+)/ContactUsCreate/$',views.ContactUsCreateView,name='contactus_create'),
    re_path(r'^(?P<pk>\d+)/ContactUsEdit/$',views.ContactUsEditView,name='contactus_edit'),
    re_path(r'^(?P<pk>\d+)/ContactUs/$',views.ContactUsView,name='contactus'),

    re_path(r'^(?P<pk>\d+)/ImageCreate/$',views.ImageCreateView,name='image_create'),
    re_path(r'^ImageList$',views.ImageListView,name='image_list'),
    re_path(r'^(?P<pk>\d+)/ImageDelete$',views.ImageDeleteView,name='image_delete'),
    re_path(r'^(?P<pk>\d+)/ImageEdit$',views.ImageEditView,name='image_edit'),
]
