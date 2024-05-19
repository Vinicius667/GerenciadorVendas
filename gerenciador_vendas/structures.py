import logging

import globals
import pandas as pd


class InfoContainer:
    def __init__(self, was_found, necessary_keys, **kwargs):
        self.was_found = was_found
        aux_dict = {}
        missing_keys = []
        for key in necessary_keys:
            if key in kwargs:
                aux_dict[key] = str(kwargs[key])
            else:
                missing_keys.append(key)
                aux_dict[key] = ""
        self.__dict__.update(aux_dict)
        if missing_keys and was_found:
            logging.warning(f"Missing keys: {', '.join(missing_keys)}")

    def __repr__(self) -> str:
        return_str = f"{self.__class__.__name__}("
        for key, value in self.__dict__.items():
            return_str += f"{key}={value}, "
        return return_str[:-2] + ")"

    def __str__(self) -> str:
        return self.__repr__()


class UserInfo(InfoContainer):
    def __init__(self, was_found, **kwargs):
        super().__init__(
            was_found, globals.USER_TABLE_COLUMNS_NAMES_TYPES.keys(), **kwargs
        )


class ProductInfo(InfoContainer):
    def __init__(self, was_found, **kwargs):
        params = list(globals.PRODUCT_TABLE_COLUMNS_NAMES_TYPES.keys()) + list(
            globals.PRICES_TABLE_COLUMNS_NAMES_TYPES.keys()
        )
        super().__init__(
            was_found,
            params,
            **kwargs,
        )


class ProductsList:
    def __init__(self):
        self.products: list[ProductInfo] = []

    def __repr__(self) -> str:
        return_str = f"{self.__class__.__name__}("
        for product in self.products:
            return_str += f"{product.nome}, "  # type: ignore
        return return_str[:-2] + ")"

    def get_table(self) -> pd.DataFrame:
        return pd.DataFrame([product.__dict__ for product in self.products])

    def append(self, product: ProductInfo):
        self.products.append(product)

    def delete(self, produto_id: int):
        for product in self.products:
            if product.nome == produto_id:  # type: ignore
                self.products.remove(product)
                return True
        return False

    def __iter__(self):
        return iter(self.products)

    def __getitem__(self, index):
        return self.products[index]

    def __len__(self):
        return len(self.products)

    def __str__(self) -> str:
        return self.__repr__()


class SaleInfo(InfoContainer):
    def __init__(self):
        self.dict_product = {}

    def add_new_product(self, produto_id: int, quantidade: int, **kwargs):
        if produto_id not in self.dict_product:
            self.dict_product[produto_id] = {"quantidade": quantidade, **kwargs}
        else:
            self.dict_product[produto_id]["quantidade"] += quantidade
    
    # implement IN operator
    def __contains__(self, produto_id: int):
        return produto_id in self.dict_product
