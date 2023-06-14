from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users/",views.getUsers, name="get users"),
    path("user/<int:id>",views.getUserById, name="get user by id"),
    path("deleteUser/<int:id>",views.deleteUserById,name="delete user"),
    path("updateUser/<int:id>",views.updateUser,name="update user"),
    path("createUser/",views.createUser,name="create user"),
    path("products/",views.getProducts, name="get products"),
    path("products/<str:category>",views.getProductByCategory,name="get products by category"),
    path("updateProduct/<int:id>",views.updateProduct,name="update user"),
    path("createProduct/",views.createProduct,name="create product"),
    path("deleteProduct/<int:id>",views.deleteProductById,name="delete product"),
    path("panier/<int:id>",views.getPanier,name="get products in the panier of a user"),
    path("panier/<int:id_utilisateur>/<int:id_produit>",views.addOrRemoveInPanier,name="add or remove product to Panier"),
    path("commandes/<int:id>",views.getCommande,name="get commande of an user"),
    path("commande/<int:utilisateur_id>/<int:produit_id>",views.addOrRemoveCommande, name="Add or Remove product to commande")
]
