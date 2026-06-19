sql_schema = pd.io.sql.get_schema(df, "my_table_name")
print(sql_schema)

df.to_sql('users', con=engine, if_exists='append', index=False)