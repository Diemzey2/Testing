from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, JSON, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.sqlite import DATETIME

# Crear el engine, que es el punto de entrada para la base de datos
engine = create_engine('sqlite:///productos.db', echo=True)

# Crear una clase base para los modelos
Base = declarative_base()

# Definir el modelo Producto
class Producto(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    temperature = Column(Integer, nullable=True)  # Usado para la 'temperatura' de las ofertas en Promodescuentos
    link = Column(String)
    merchant_name = Column(String, nullable=True)
    published_at = Column(DateTime, nullable=True)  # Almacenar fechas con tiempo en SQLite usando DATETIME
    old_price = Column(Float, nullable=True)
    price = Column(Float)
    imgurl = Column(String)
    source = Column(String)  # Columna para la fuente
    additional_info = Column(JSON)  # Campo JSON para almacenar información adicional como 'mensualidades' y 'envio_gratis'

# Crear las tablas en la base de datos
Base.metadata.create_all(engine)

# Crear una sesión para interactuar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()
