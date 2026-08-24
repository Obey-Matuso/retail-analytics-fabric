[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "Query_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared Query = let
  Source = Json.Document(Web.Contents("https://dummyjson.com/products/category/smartphones")),
  #"Converted to table" = Table.FromRecords({Source}),
  #"Expanded products" = Table.ExpandListColumn(#"Converted to table", "products"),
  #"Expanded products1" = Table.ExpandRecordColumn(#"Expanded products", "products", {"id", "title", "description", "category", "price", "discountPercentage", "rating", "stock", "tags", "brand", "sku", "weight", "dimensions", "warrantyInformation", "shippingInformation", "availabilityStatus", "reviews", "returnPolicy", "minimumOrderQuantity", "meta", "images", "thumbnail"}, {"products.id", "products.title", "products.description", "products.category", "products.price", "products.discountPercentage", "products.rating", "products.stock", "products.tags", "products.brand", "products.sku", "products.weight", "products.dimensions", "products.warrantyInformation", "products.shippingInformation", "products.availabilityStatus", "products.reviews", "products.returnPolicy", "products.minimumOrderQuantity", "products.meta", "products.images", "products.thumbnail"}),
  #"Split column" = Table.SplitColumn(#"Expanded products1", "products.tags", each _, {"products.tags.0", "products.tags.1"}),
  #"Expanded products.dimensions" = Table.ExpandRecordColumn(#"Split column", "products.dimensions", {"width", "height", "depth"}, {"products.dimensions.width", "products.dimensions.height", "products.dimensions.depth"}),
  #"Expanded products.meta" = Table.ExpandRecordColumn(#"Expanded products.dimensions", "products.meta", {"createdAt", "updatedAt", "barcode", "qrCode"}, {"products.meta.createdAt", "products.meta.updatedAt", "products.meta.barcode", "products.meta.qrCode"}),
  #"Changed column type" = Table.TransformColumnTypes(#"Expanded products.meta", {{"products.id", Int64.Type}, {"products.title", type text}, {"products.description", type text}, {"products.category", type text}, {"products.price", type number}, {"products.discountPercentage", type number}, {"products.rating", type number}, {"products.stock", Int64.Type}, {"products.tags.0", type text}, {"products.tags.1", type text}, {"products.brand", type text}, {"products.sku", type text}, {"products.weight", Int64.Type}, {"products.dimensions.width", type number}, {"products.dimensions.height", type number}, {"products.dimensions.depth", type number}, {"products.warrantyInformation", type text}, {"products.shippingInformation", type text}, {"products.availabilityStatus", type text}, {"products.returnPolicy", type text}, {"products.minimumOrderQuantity", Int64.Type}, {"products.meta.createdAt", type datetime}, {"products.meta.updatedAt", type datetime}, {"products.meta.barcode", Int64.Type}, {"products.meta.qrCode", type text}, {"products.thumbnail", type text}, {"total", Int64.Type}, {"skip", Int64.Type}, {"limit", Int64.Type}})
in
  #"Changed column type";
shared Query_DataDestination = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true]),
  Navigation_1 = Pattern{[workspaceId = "f16ab152-d476-4d68-9ca9-80c3d2d310b5"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "5b2c63ee-d263-444e-a47c-99827cd9783b"]}[Data],
  Navigation_3 = Navigation_2{[Id = "dbo", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "raw_products", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;
