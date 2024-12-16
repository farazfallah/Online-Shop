<script>
    import Layout from '../layouts/Layout.svelte';
</script>

<Layout title="Home">
    <main>
        <slot>
            <h1>Welcome to the Home Page</h1>
            <p>This is the main content of the page.</p>
        </slot> <!-- محتویات صفحه در اینجا قرار می‌گیرد -->
    </main>
</Layout>

<main>
    <slot>
        <h1>Welcome to the Home Page</h1>
        <p>This is the main content of the page.</p>
    </slot> <!-- محتویات صفحه در اینجا قرار می‌گیرد -->
</main>