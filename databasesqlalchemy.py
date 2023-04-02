from sqlalchemy import create_engine, text

db_connection_string = "mariadb+pymysql://pfhb29t06w6px7ueuirc:pscale_pw_CUUpIyII7FSKkeebXGgdMhGGrdGZLMrmGNuNHQmXaZB@aws.connect.psdb.cloud/centralgarageadmin?charset=utf8mb4"

engine = create_engine(
  db_connection_string,
  connect_args={
    "ssl": {
      "ssl_ca": "/etc/ssl/cert.pem"
      }
  })

with engine.connect() as conn:
  result = conn.execute(text("SELECT * FROM InvoiceHeader"))
  print(result.all())
