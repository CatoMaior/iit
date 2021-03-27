N = 35
J = -1
H = 0
Kb = 1
trigger = 30000
sample_delay = 500
n_samples = 300

S = [[rand(-1:2:1) for i = 1:N] for j = 1:N]

function getΔE(x, y)
	lowerX = x - 1
	upperX = x + 1
	lowerY = y - 1
	upperY = y + 1
	if x - 1 == 0 lowerX = N
	elseif x + 1 > N upperX = 1 end
	if y - 1 == 0 lowerY = N
	elseif y + 1 > N upperY = 1 end
    ΔE = -2 * J * S[x][y] * (S[upperX][y] + S[x][upperY] +
                      S[lowerX][y] + S[x][lowerY])
    return ΔE
end

function run_cycles(T)
    m_arr_loc = []
    for i = 1 : (trigger + n_samples * sample_delay)
        m_loc = 0
        x = rand(1 : N)
        y = rand(1 : N)
        ΔE = getΔE(x, y)

        if (ΔE < 0) | (rand() < exp(-ΔE / (Kb * T)))
            S[x][y] *= -1
        end

        if (i % sample_delay == 0) & (i > trigger)
            for j = 1:N, k = 1:N
                m_loc += S[j][k]
            end
            append!(m_arr_loc, m_loc / N ^ 2)
        end
    end
	magn = 0
    for i = 1:n_samples
		magn += m_arr_loc[i]
	end
	magn /= n_samples
	magn = abs(magn)
	return magn
end

res_arr = []
temp_arr = []

function go()
	for t = 0.01:0.01:4
		append!(res_arr, run_cycles(t))
		append!(temp_arr, t)
	end
end

@time(go())

using Plots
plot(temp_arr, res_arr)
