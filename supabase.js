importar { createClient } de '@supabase/supabase-js'

const supabaseUrl = processo . env .REACT_APP_SUPABASE_URL
const supabaseKey = processo . env . REACT_APP_ANON_KEY
const supabase = createClient ( supabaseUrl , supabaseKey )

export default supabase