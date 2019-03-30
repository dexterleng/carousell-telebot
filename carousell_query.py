import requests
import json

class CarousellQuery:
  def __init__(self, keyword):
    self.keyword = keyword
    self.query_url = "https://sg.carousell.com/search/products/?query={}&sort_by=time_created%2Cdescending".format(keyword)
    self.response = requests.get(self.query_url)
    self.html_str = self.response.content.decode("utf-8")
    self.products = parse_products(self.html_str)

  # returns all new products since last_sent_product_id in reverse chronological order
  def get_new_products(self, last_sent_product_id):
    if last_sent_product_id is None:
      return self.products
    for i in range(len(self.products)):
      product = self.products[i]
      if product['id'] == last_sent_product_id:
        return self.products[:i]
    return self.products
  

def parse_products(html_str):
  product_by_id = get_products_map(html_str)
  products_browse_ids = get_products_browse_ids(html_str)
  return list(map(lambda id: product_by_id[id], products_browse_ids))

# returns product_id -> product dictionary
def get_products_map(html_str):
  start_index = html_str.find('"productsMap":{')
  if start_index == -1:
    raise Exception("Cannot find \"productsMap\" key.")
  first_brace_index = start_index + len('"productsMap":{') - 1
  last_brace_index = find_last_brace_index(first_brace_index, html_str)
  products_map_str = html_str[first_brace_index:last_brace_index + 1]
  products_map_dict = json.loads(products_map_str)
  return products_map_dict

# returns array of product_ids in reverse chronological order
def get_products_browse_ids(html_str):
  start_index = html_str.find('"PRODUCTS_BROWSE":[')
  if start_index == -1:
    raise Exception("Cannot find \"PRODUCTS_BROWSE\" key.")
  opening_bracket_index = start_index + len('"PRODUCTS_BROWSE":[') - 1
  if html_str[opening_bracket_index] != "[":
    raise Exception("opening_bracket_index is not an opening bracket ([).")
  closing_bracket_index = opening_bracket_index + 1
  while html_str[closing_bracket_index] != "]":
    closing_bracket_index += 1
  products_browse_str = html_str[opening_bracket_index:closing_bracket_index + 1]
  products_browse_ids = json.loads(products_browse_str)
  return products_browse_ids

def find_last_brace_index(first_brace_index, html_str):
  if html_str[first_brace_index] != "{":
    raise Exception("first_brace_index is not an opening brace ({).")

  stack = ["{"]
  i = first_brace_index + 1
  while len(stack) > 0:
    char = html_str[i]
    if char == '"':
      if stack[-1] == '"':
        stack.pop()
      else:
        stack.append('"')
    # ignore if it is an escaped quote by double incrementing
    elif char == '\\' and html_str[i + 1] == '"':
      i += 1
    elif char == '{':
      if stack[-1] != '"':
        stack.append('{')
    elif char == '}':
      if stack[-1] == '{':
        stack.pop()
    i += 1
  return i - 1
