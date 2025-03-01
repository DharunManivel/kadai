import folium
import json

# Load data
with open('restaurants-places_priority.json', 'r', encoding='utf-8') as f:
    restaurants = json.load(f)

# Create map
m = folium.Map(location=[11.1271, 78.6569], zoom_start=7)

# Add markers
for restaurant in restaurants:
    if 'lat' not in restaurant or 'lng' not in restaurant:
        continue
    print(f"{restaurant['name']}")
    # Generate directions URL
    directions_url = f"{restaurant['link']}"


    # Generate phone link
    phone_html = f"<a href='tel:{restaurant['phone']}'>{restaurant['phone']}</a>" if restaurant.get('phone') else 'Not available'

    # Popup HTML
    popup_html = f"""
    <div style="width: 250px;">
        <h3>{restaurant['name']}</h3>
        <p><b>Specialty:</b> {restaurant['special']}</p>
        <p><b>Rating:</b> {restaurant.get('rating', 'N/A')} ⭐ ({restaurant.get('reviews', 0)} reviews)</p>
        <p><b>Phone:</b> {phone_html}</p>
        <a href="{directions_url}" target="_blank"
           style="display: block; padding: 5px; background: #4285f4; color: white; text-align: center; border-radius: 5px;">
            Get Directions
        </a>
    </div>
    """
    # print( f"{restaurant['lat']} , {restaurant['lng']}")
    # Add marker
    folium.Marker(
        location=[restaurant['lat'], restaurant['lng']],
        popup=folium.Popup(popup_html, max_width=300),
        icon=folium.Icon(color='red', icon='cutlery', prefix='fa')
    ).add_to(m)

# Save map
m.save('tamilnadu_restaurants_map.html')
