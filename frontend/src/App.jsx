import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

export default function App() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [formData, setFormData] = useState({
    product_name: '',
    brands: '',
    price: '',
    stock: '',
  })
  const [editingId, setEditingId] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')

  // Fetch all items
  useEffect(() => {
    fetchItems()
  }, [])

  const fetchItems = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get('/inventory')
      setItems(response.data)
    } catch (err) {
      setError('Failed to fetch items')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleAddItem = async (e) => {
    e.preventDefault()
    if (!formData.product_name.trim()) {
      setError('Product name is required')
      return
    }

    try {
      const payload = {
        product_name: formData.product_name,
        brands: formData.brands || '',
        price: parseFloat(formData.price) || 0,
        stock: parseInt(formData.stock) || 0,
      }
      await axios.post('/inventory', payload)
      setFormData({ product_name: '', brands: '', price: '', stock: '' })
      fetchItems()
    } catch (err) {
      setError('Failed to add item')
      console.error(err)
    }
  }

  const handleUpdateItem = async (id) => {
    try {
      const payload = {}
      if (formData.price) payload.price = parseFloat(formData.price)
      if (formData.stock) payload.stock = parseInt(formData.stock)

      if (Object.keys(payload).length === 0) {
        setError('Enter a price or stock value to update')
        return
      }

      await axios.patch(`/inventory/${id}`, payload)
      setEditingId(null)
      setFormData({ product_name: '', brands: '', price: '', stock: '' })
      fetchItems()
    } catch (err) {
      setError('Failed to update item')
      console.error(err)
    }
  }

  const handleDeleteItem = async (id) => {
    if (window.confirm('Delete this item?')) {
      try {
        await axios.delete(`/inventory/${id}`)
        fetchItems()
      } catch (err) {
        setError('Failed to delete item')
        console.error(err)
      }
    }
  }

  const handleSearchOpenFoodFacts = async () => {
    if (!searchQuery.trim()) {
      setError('Enter a product name to search')
      return
    }
    try {
      const response = await axios.get('/inventory/search', {
        params: { name: searchQuery },
      })
      setFormData({
        product_name: response.data.product_name || '',
        brands: response.data.brands || '',
        price: '',
        stock: '',
      })
      setSearchQuery('')
    } catch (err) {
      setError('Product not found on OpenFoodFacts')
      console.error(err)
    }
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Inventory Manager</h1>
        <p>Manage your retail inventory with ease</p>
      </header>

      {error && <div className="error-banner">{error}</div>}

      <main className="app-main">
        {/* Add/Edit Form */}
        <section className="form-section">
          <h2>{editingId ? `Edit Item #${editingId}` : 'Add New Item'}</h2>
          <form onSubmit={editingId ? undefined : handleAddItem} className="item-form">
            <div className="form-group">
              <label>Product Name</label>
              <input
                type="text"
                value={formData.product_name}
                onChange={(e) => setFormData({ ...formData, product_name: e.target.value })}
                placeholder="e.g., Organic Almond Milk"
                disabled={editingId !== null}
              />
            </div>

            <div className="form-group">
              <label>Brand</label>
              <input
                type="text"
                value={formData.brands}
                onChange={(e) => setFormData({ ...formData, brands: e.target.value })}
                placeholder="e.g., Silk"
                disabled={editingId !== null}
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label>Price</label>
                <input
                  type="number"
                  step="0.01"
                  value={formData.price}
                  onChange={(e) => setFormData({ ...formData, price: e.target.value })}
                  placeholder="0.00"
                />
              </div>
              <div className="form-group">
                <label>Stock</label>
                <input
                  type="number"
                  value={formData.stock}
                  onChange={(e) => setFormData({ ...formData, stock: e.target.value })}
                  placeholder="0"
                />
              </div>
            </div>

            {editingId ? (
              <div className="form-actions">
                <button
                  type="button"
                  onClick={() => handleUpdateItem(editingId)}
                  className="btn btn-primary"
                >
                  Save Changes
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setEditingId(null)
                    setFormData({ product_name: '', brands: '', price: '', stock: '' })
                  }}
                  className="btn btn-secondary"
                >
                  Cancel
                </button>
              </div>
            ) : (
              <button type="submit" className="btn btn-primary">
                Add Item
              </button>
            )}
          </form>

          {/* Search OpenFoodFacts */}
          <div className="search-section">
            <h3>Search OpenFoodFacts</h3>
            <div className="search-bar">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Enter product name..."
              />
              <button onClick={handleSearchOpenFoodFacts} className="btn btn-secondary">
                Search
              </button>
            </div>
          </div>
        </section>

        {/* Items Grid */}
        <section className="items-section">
          <h2>Inventory ({items.length} items)</h2>
          {loading && <p className="loading">Loading...</p>}
          {items.length === 0 && !loading && (
            <p className="empty-state">No items yet. Add one to get started.</p>
          )}
          <div className="items-grid">
            {items.map((item) => (
              <div key={item.id} className="item-card">
                <div className="item-header">
                  <h3>{item.product_name}</h3>
                  <span className="item-id">#{item.id}</span>
                </div>
                <p className="item-brand">{item.brands || 'No brand'}</p>
                <div className="item-details">
                  <div className="detail">
                    <span className="label">Price</span>
                    <span className="value">${item.price.toFixed(2)}</span>
                  </div>
                  <div className="detail">
                    <span className="label">Stock</span>
                    <span className="value">{item.stock} units</span>
                  </div>
                </div>
                <div className="item-actions">
                  <button
                    onClick={() => {
                      setEditingId(item.id)
                      setFormData({ product_name: '', brands: '', price: '', stock: '' })
                    }}
                    className="btn btn-sm btn-secondary"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDeleteItem(item.id)}
                    className="btn btn-sm btn-danger"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  )
}